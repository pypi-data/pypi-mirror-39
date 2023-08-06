.. sectionauthor:: Dan Blanchard <dblanchard@ets.org>

Running Experiments
===================
The simplest way to use SKLL is to create configuration files that describe
experiments you would like to run on pre-generated features. This document
describes the supported feature file formats, how to create configuration files
(and layout your directories), and how to use
:ref:`run_experiment <run_experiment>` to get things going.

Quick Example
-------------
If you don't want to read the whole document, and just want an example of how
things work, do the following from the command prompt:

.. code-block:: bash

    $ cd examples
    $ python make_iris_example_data.py          # download a simple dataset
    $ cd iris
    $ run_experiment --local evaluate.cfg        # run an experiment


.. _file_formats:

Feature file formats
--------------------
The following feature file formats are supported:

.. _arff:

arff
^^^^
The same file format used by `Weka <https://www.cs.waikato.ac.nz/ml/weka/>`__
with the following added restrictions:

*   Only simple numeric, string, and nomimal values are supported.
*   Nominal values are converted to strings.
*   If the data has instance IDs, there should be an attribute with the name
    specified by :ref:`id_col <id_col>` in the :ref:`Input` section of the configuration file you create for your experiment. This defaults to ``id``.  If there is no such attribute, IDs will be generated automatically.
*   If the data is labelled, there must be an attribute with the name specified
    by :ref:`label_col <label_col>` in the :ref:`Input` section of the
    configuartion file you create for your experiment. This defaults to ``y``.
    This must also be the final attribute listed (like in Weka).

.. _csv:

csv/tsv
^^^^^^^

A simple comma or tab-delimited format with the following restrictions:

*   If the data is labelled, there must be a column with the name
    specified by :ref:`label_col <label_col>` in the :ref:`Input` section of the
    configuartion file you create for your experiment. This defaults to
    ``y``.
*   If the data has instance IDs, there should be a column with the name
    specified by :ref:`id_col <id_col>` in the :ref:`Input` section of the configuration file you create for your experiment. This defaults to ``id``.  If there is no such column, IDs will be generated automatically.
*   All other columns contain feature values, and every feature value
    must be specified (making this a poor choice for sparse data).

.. _ndj:

jsonlines/ndj *(Recommended)*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A twist on the `JSON <http://www.json.org/>`__ format where every line is a
either JSON dictionary (the entire contents of a normal JSON file), or a
comment line starting with ``//``. Each dictionary is expected to contain the
following keys:

*   **y**: The class label.
*   **x**: A dictionary of feature values.
*   **id**: An optional instance ID.

This is the preferred file format for SKLL, as it is sparse and can be slightly
faster to load than other formats.

.. _libsvm:

libsvm
^^^^^^

While we can process the standard input file format supported by
`LibSVM <https://www.csie.ntu.edu.tw/~cjlin/libsvm/>`__,
`LibLinear <https://www.csie.ntu.edu.tw/~cjlin/liblinear/>`__,
and `SVMLight <http://svmlight.joachims.org>`__, we also support specifying
extra metadata usually missing from the format in comments at the of each line.
The comments are not mandatory, but without them, your labels and features will
not have names.  The comment is structured as follows::

    ID | 1=ClassX | 1=FeatureA 2=FeatureB

The entire format would like this::

    2 1:2.0 3:8.1 # Example1 | 2=ClassY | 1=FeatureA 3=FeatureC
    1 5:7.0 6:19.1 # Example2 | 1=ClassX | 5=FeatureE 6=FeatureF

.. note::
    IDs, labels, and feature names cannot contain the following
    characters:  ``|`` ``#`` ``=``

.. _megam:

megam
^^^^^

An expanded form of the input format for the
`MegaM classification package <http://users.umiacs.umd.edu/~hal/megam/>`__ with
the ``-fvals`` switch.

The basic format is::

    # Instance1
    CLASS1    F0 2.5 F1 3 FEATURE_2 -152000
    # Instance2
    CLASS2    F1 7.524

where the **optional** comments before each instance specify the ID for the
following line, class names are separated from feature-value pairs with a tab,
and feature-value pairs are separated by spaces. Any omitted features for a
given instance are assumed to be zero, so this format is handy when dealing
with sparse data. We also include several utility scripts for converting
to/from this MegaM format and for adding/removing features from the files.

.. _create_config:

Creating configuration files
----------------------------
The experiment configuration files that run_experiment accepts are standard
`Python configuration files <https://docs.python.org/2/library/configparser.html>`__
that are similar in format to Windows INI files. [#]_
There are four expected sections in a configuration file: :ref:`General`,
:ref:`Input`, :ref:`Tuning`, and :ref:`Output`.  A detailed description of each
possible settings for each section is provided below, but to summarize:

.. _cross_validate:

*   If you want to do **cross-validation**, specify a path to training feature
    files, and set :ref:`task` to ``cross_validate``. Please note that the
    cross-validation currently uses
    `StratifiedKFold <https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html>`__.
    You also can optionally use predetermined folds with the
    :ref:`folds_file <folds_file>` setting.

    .. note::

        When using classifiers, SKLL will automatically reduce the
        number of cross-validation folds to be the same as the minimum
        number of examples for any of the classes in the training data.


.. _evaluate:

*   If you want to **train a model and evaluate it** on some data, specify a
    training location, a test location, and a directory to store results,
    and set :ref:`task` to ``evaluate``.

.. _predict:

*   If you want to just **train a model and generate predictions**, specify
    a training location, a test location, and set :ref:`task` to ``predict``.

.. _train:

*   If you want to just **train a model**, specify a training location, and set
    :ref:`task` to ``train``.

.. _learning_curve:

*   If you want to **generate a learning curve** for your data, specify a training location and set :ref:`task` to ``learning_curve``. The learning curve is generated using essentially the same underlying process as in `scikit-learn <https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.learning_curve.html#sklearn.model_selection.learning_curve>`__ except that the SKLL feature pre-processing pipline is used while training the various models and computing the scores.

    .. note::

        Ideally, one would first do cross-validation experiments with grid search and/or ablation and get a well-performing set of features and hyper-parameters for a set of learners. Then, one would explicitly specify those features (via :ref:`featuresets <featuresets>`) and hyper-parameters (via :ref:`fixed_parameters <fixed_parameters>`) in the config file for the learning curve and explore the impact of the size of the training data.

.. _learners_required:

*   A :ref:`list of classifiers/regressors <learners>` to try on your feature
    files is required.

Example configuration files are available `here <https://github.com/EducationalTestingService/skll/tree/master/examples/>`__.

.. _general:

General
^^^^^^^

Both fields in the General section are required.

.. _experiment_name:

experiment_name
"""""""""""""""

A string used to identify this particular experiment configuration. When
generating result summary files, this name helps prevent overwriting previous
summaries.

.. _task:

task
""""

What types of experiment we're trying to run. Valid options are:
:ref:`cross_validate <cross_validate>`, :ref:`evaluate <evaluate>`,
:ref:`predict <predict>`, :ref:`train <train>`, :ref:`learning_curve <learning_curve>`.

.. _input:

Input
^^^^^

The Input section has only one required field, :ref:`learners`, but also must
contain either :ref:`train_file <train_file>` or
:ref:`train_directory <train_directory>`.

.. _learners:

learners
""""""""
List of scikit-learn models to try using. A separate job will be run for each
combination of classifier and feature-set. Acceptable values are described
below.  Custom learners can also be specified. See
:ref:`custom_learner_path <custom_learner_path>`.

.. _classifiers:

Classifiers:

    *   **AdaBoostClassifier**: `AdaBoost Classification <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html#sklearn.ensemble.AdaBoostClassifier>`__.  Note that the default base estimator is a ``DecisionTreeClassifier``. A different base estimator can be used by specifying a ``base_estimator`` fixed parameter in the :ref:`fixed_parameters <fixed_parameters>` list. The following additional base estimators are supported: ``MultinomialNB``, ``SGDClassifier``, and ``SVC``. Note that the last two base require setting an additional ``algorithm`` fixed parameter with the value ``'SAMME'``.
    *   **DummyClassifier**: `Simple rule-based Classification <https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html#sklearn.dummy.DummyClassifier>`__
    *   **DecisionTreeClassifier**: `Decision Tree Classification <https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier>`__
    *   **GradientBoostingClassifier**: `Gradient Boosting Classification <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier>`__
    *   **KNeighborsClassifier**: `K-Nearest Neighbors Classification <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier>`__
    *   **LinearSVC**: `Support Vector Classification using LibLinear <https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC>`__
    *   **LogisticRegression**: `Logistic Regression Classification using LibLinear <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression>`__
    *   **MLPClassifier**: `Multi-layer Perceptron Classification <https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier>`__
    *   **MultinomialNB**: `Multinomial Naive Bayes Classification <https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html#sklearn.naive_bayes.MultinomialNB>`__
    *   **RandomForestClassifier**: `Random Forest Classification <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier>`__
    *   **RidgeClassifier**: `Classification using Ridge Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html#sklearn.linear_model.RidgeClassifier>`__
    *   **SGDClassifier**: `Stochastic Gradient Descent Classification <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html>`__
    *   **SVC**: `Support Vector Classification using LibSVM <https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC>`__

.. _regressors:

Regressors:

    *   **AdaBoostRegressor**: `AdaBoost Regression <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostRegressor.html#sklearn.ensemble.AdaBoostRegressor>`__. Note that the default base estimator is a ``DecisionTreeRegressor``. A different base estimator can be used by specifying a ``base_estimator`` fixed parameter in the :ref:`fixed_parameters <fixed_parameters>` list. The following additional base estimators are supported: ``SGDRegressor``, and ``SVR``.
    *   **BayesianRidge**: `Bayesian Ridge Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.BayesianRidge.html#sklearn.linear_model.BayesianRidge>`__
    *   **DecisionTreeRegressor**: `Decision Tree Regressor <https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html#sklearn.tree.DecisionTreeRegressor>`__
    *   **DummyRegressor**: `Simple Rule-based Regression <https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html#sklearn.dummy.DummyRegressor>`__
    *   **ElasticNet**: `ElasticNet Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html#sklearn.linear_model.ElasticNet>`__
    *   **GradientBoostingRegressor**: `Gradient Boosting Regressor <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html#sklearn.ensemble.GradientBoostingRegressor>`__
    *   **HuberRegressor**: `Huber Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html#sklearn.linear_model.HuberRegressor>`__
    *   **KNeighborsRegressor**: `K-Nearest Neighbors Regression <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html#sklearn.neighbors.KNeighborsRegressor>`__
    *   **Lars**: `Least Angle Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lars.html#sklearn.linear_model.Lars>`__
    *   **Lasso**: `Lasso Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso>`__
    *   **LinearRegression**: `Linear Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression>`__
    *   **LinearSVR**: `Support Vector Regression using LibLinear <https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVR.html#sklearn.svm.LinearSVR>`__
    *   **MLPRegressor**: `Multi-layer Perceptron Regression <https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor>`__
    *   **RandomForestRegressor**: `Random Forest Regression <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html#sklearn.ensemble.RandomForestRegressor>`__
    *   **RANSACRegressor**: `RANdom SAmple Consensus Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html#sklearn.linear_model.RANSACRegressor>`__. Note that the default base estimator is a ``LinearRegression``. A different base regressor can be used by specifying a ``base_estimator`` fixed parameter in the :ref:`fixed_parameters <fixed_parameters>` list.
    *   **Ridge**: `Ridge Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge>`__
    *   **SGDRegressor**: `Stochastic Gradient Descent Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html>`__
    *   **SVR**: `Support Vector Regression using LibSVM <https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html#sklearn.svm.SVR>`__
    *   **TheilSenRegressor**: `Theil-Sen Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TheilSenRegressor.html#sklearn.linear_model.TheilSenRegressor>`__

    For all regressors you can also prepend ``Rescaled`` to the
    beginning of the full name (e.g., ``RescaledSVR``) to get a version
    of the regressor where predictions are rescaled and constrained to
    better match the training set.

.. _train_file:

train_file *(Optional)*
"""""""""""""""""""""""

Path to a file containing the features to train on.  Cannot be used in
combination with :ref:`featuresets <featuresets>`,
:ref:`train_directory <train_directory>`, or :ref:`test_directory <test_directory>`.

.. note::

    If :ref:`train_file <train_file>` is not specified,
    :ref:`train_directory <train_directory>` must be.

.. _train_directory:

train_directory *(Optional)*
""""""""""""""""""""""""""""

Path to directory containing training data files. There must be a file for each
featureset.  Cannot be used in combination with :ref:`train_file <train_file>`
or :ref:`test_file <test_file>`.

.. note::

    If :ref:`train_directory <train_directory>` is not specified,
    :ref:`train_file <train_file>` must be.

.. _test_file:

test_file *(Optional)*
""""""""""""""""""""""

Path to a file containing the features to test on.  Cannot be used in
combination with :ref:`featuresets <featuresets>`,
:ref:`train_directory <train_directory>`, or :ref:`test_directory <test_directory>`

.. _test_directory:

test_directory *(Optional)*
"""""""""""""""""""""""""""

Path to directory containing test data files. There must be a file
for each featureset.  Cannot be used in combination with
:ref:`train_file <train_file>` or :ref:`test_file <test_file>`.

.. _featuresets:

featuresets *(Optional)*
""""""""""""""""""""""""
List of lists of prefixes for the files containing the features you would like
to train/test on.  Each list will end up being a job. IDs are required to be
the same in all of the feature files, and a :py:exc:`ValueError` will be raised
if this is not the case.  Cannot be used in combination with
:ref:`train_file <train_file>` or :ref:`test_file <test_file>`.

.. note::

    If specifying :ref:`train_directory <train_directory>` or
    :ref:`test_directory <test_directory>`, :ref:`featuresets <featuresets>`
    is required.

.. _suffix:

suffix *(Optional)*
"""""""""""""""""""

The file format the training/test files are in. Valid option are
:ref:`.arff <arff>`, :ref:`.csv <csv>`, :ref:`.jsonlines <ndj>`,
:ref:`.libsvm <libsvm>`, :ref:`.megam <megam>`, :ref:`.ndj <ndj>`, and
:ref:`.tsv <csv>`.

If you omit this field, it is assumed that the "prefixes" listed in
:ref:`featuresets <featuresets>` are actually complete filenames. This can be
useful if you have feature files that are all in different formats that you
would like to combine.


.. _id_col:

id_col *(Optional)*
"""""""""""""""""""
If you're using :ref:`ARFF <arff>`, :ref:`CSV <csv>`, or :ref:`TSV <csv>`
files, the IDs for each instance are assumed to be in a column with this
name. If no column with this name is found, the IDs are generated
automatically. Defaults to ``id``.

.. _label_col:

label_col *(Optional)*
""""""""""""""""""""""

If you're using :ref:`ARFF <arff>`, :ref:`CSV <csv>`, or :ref:`TSV <csv>`
files, the class labels for each instance are assumed to be in a column with
this name. If no column with this name is found, the data is assumed to be
unlabelled. Defaults to ``y``. For ARFF files only, this must also be the final
column to count as the label (for compatibility with Weka).

.. _ids_to_floats:

ids_to_floats *(Optional)*
""""""""""""""""""""""""""

If you have a dataset with lots of examples, and your input files have IDs that
look like numbers (can be converted by float()), then setting this to True will
save you some memory by storing IDs as floats. Note that this will cause IDs to
be printed as floats in prediction files (e.g., ``4.0`` instead of ``4`` or
``0004`` or ``4.000``).

.. _shuffle:

shuffle *(Optional)*
""""""""""""""""""""

If ``True``, shuffle the examples in the training data before using them for
learning. This happens automatically when doing a grid search but it might be
useful in other scenarios as well, e.g., online learning. Defaults to
``False``.

.. _class_map:

class_map *(Optional)*
""""""""""""""""""""""

If you would like to collapse several labels into one, or otherwise modify your
labels (without modifying your original feature files), you can specify a
dictionary mapping from new class labels to lists of original class labels. For
example, if you wanted to collapse the labels ``beagle`` and ``dachsund`` into a
``dog`` class, you would specify the following for ``class_map``:

.. code-block:: python

   {'dog': ['beagle', 'dachsund']}

Any labels not included in the dictionary will be left untouched.

.. _num_cv_folds:

num_cv_folds *(Optional)*
"""""""""""""""""""""""""

The number of folds to use for cross validation. Defaults to 10.

.. _random_folds:

random_folds *(Optional)*
"""""""""""""""""""""""""

Whether to use random folds for cross-validation. Defaults to ``False``.

.. _folds_file:

folds_file *(Optional)*
""""""""""""""""""""""""""""""

Path to a csv file specifying the mapping of instances in the training data
to folds. This can be specified when the :ref:`task` is either ``train`` or
``cross_validate``. For the ``train`` task, if :ref:`grid_search <grid_search>`
is ``True``, this file, if specified, will be used to define the
cross-validation used for the grid search (leave one fold ID out at a time).
Otherwise, it will be ignored.

For the ``cross_validate`` task, this file will be used to define the outer
cross-validation loop and, if :ref:`grid_search <grid_search>` is ``True``, also for the
inner grid-search cross-validation loop. If the goal of specifiying the folds
file is to ensure that the model does not learn to differentiate based on a confound:
e.g. the data from the same person is always in the same fold, it makes sense to
keep the same folds for both the outer and the inner cross-validation loops.

However, sometimes the goal of specifying the folds file is simply for the
purpose of comparison to another existing experiment or another context
in which maintaining the constitution of the folds in the inner
grid-search loop is not required. In this case, users may set the parameter
:ref:`use_folds_file_for_grid_search <use_folds_file_for_grid_search>`
to ``False`` which will then direct the inner grid-search cross-validation loop
to simply use the number specified via :ref:`grid_search_folds <grid_search_folds>`
instead of using the folds file. This will likely lead to shorter execution times as
well depending on how many folds are in the folds file and the value
of :ref:`grid_search_folds <grid_search_folds>`.

The format of this file must be as follows: the first row must be a header.
This header row is ignored, so it doesn't matter what the header row contains,
but it must be there. If there is no header row, whatever row is in its place
will be ignored. The first column should consist of training set IDs and the
second should be a string for the fold ID (e.g., 1 through 5, A through D, etc.).
If specified, the CV and grid search will leave one fold ID out at a time. [#]_

.. _learning_curve_cv_folds_list:

learning_curve_cv_folds_list *(Optional)*
""""""""""""""""""""""""""""""""""""""""""

List of integers specifying the number of folds to use for cross-validation
at each point of the learning curve (training size), one per learner. For
example, if you specify the following learners: ``["SVC", "LogisticRegression"]``,
specifying ``[10, 100]`` as the value of ``learning_curve_cv_folds_list`` will
tell SKLL to use 10 cross-validation folds at each point of the SVC curve and
100 cross-validation folds at each point of the logistic regression curve. Although
more folds will generally yield more reliable results, smaller number of folds
may be better for learners that are slow to train. Defaults to 10 for
each learner.

.. _learning_curve_train_sizes:

learning_curve_train_sizes *(Optional)*
""""""""""""""""""""""""""""""""""""""""""

List of floats or integers representing relative or absolute numbers
of training examples that will be used to generate the learning curve
respectively. If the type is float, it is regarded as a fraction of
the maximum size of the training set (that is determined by the selected
validation method), i.e. it has to be within (0, 1]. Otherwise it is
interpreted as absolute sizes of the training sets. Note that for classification
the number of samples usually have to be big enough to contain at least
one sample from each class. Defaults to ``[0.1, 0.325, 0.55, 0.775, 1.0]``.

.. _custom_learner_path:

custom_learner_path *(Optional)*
""""""""""""""""""""""""""""""""

Path to a ``.py`` file that defines a custom learner.  This file will be
imported dynamically.  This is only required if a custom learner is specified
in the list of :ref:`learners`.

All Custom learners must implement the ``fit`` and
``predict`` methods. Custom classifiers must either (a) inherit from an existing scikit-learn classifier, or (b) inherit from both `sklearn.base.BaseEstimator <https://scikit-learn.org/stable/modules/generated/sklearn.base.BaseEstimator.html>`__. *and* from `sklearn.base.ClassifierMixin <https://scikit-learn.org/stable/modules/generated/sklearn.base.ClassifierMixin.html>`__.

Similarly, Custom regressors must either (a) inherit from an existing scikit-learn regressor, or (b) inherit from both `sklearn.base.BaseEstimator <https://scikit-learn.org/stable/modules/generated/sklearn.base.BaseEstimator.html>`__. *and* from `sklearn.base.RegressorMixin <https://scikit-learn.org/stable/modules/generated/sklearn.base.RegressorMixin.html>`__.

Learners that require dense matrices should implement a method ``requires_dense``
that returns ``True``.

.. _sampler:

sampler *(Optional)*
""""""""""""""""""""

It performs a non-linear transformations of the input, which can serve
as a basis for linear classification or other algorithms. Valid options
are:
`Nystroem <https://scikit-learn.org/stable/modules/generated/sklearn.kernel_approximation.Nystroem.html#sklearn.kernel_approximation.Nystroem>`__,
`RBFSampler <https://scikit-learn.org/stable/modules/generated/sklearn.kernel_approximation.RBFSampler.html#sklearn.kernel_approximation.RBFSampler>`__,
`SkewedChi2Sampler <https://scikit-learn.org/stable/modules/generated/sklearn.kernel_approximation.SkewedChi2Sampler.html#sklearn.kernel_approximation.SkewedChi2Sampler>`__, and
`AdditiveChi2Sampler <https://scikit-learn.org/stable/modules/generated/sklearn.kernel_approximation.AdditiveChi2Sampler.html#sklearn.kernel_approximation.AdditiveChi2Sampler>`__.  For additional information see
`the scikit-learn documentation <https://scikit-learn.org/stable/modules/kernel_approximation.html>`__.

.. _sampler_parameters:

sampler_parameters *(Optional)*
"""""""""""""""""""""""""""""""

dict containing parameters you want to have fixed for  the ``sampler``.
Any empty ones will be ignored (and the defaults will be used).

The default fixed parameters (beyond those that scikit-learn sets) are:

Nystroem
    .. code-block:: python

       {'random_state': 123456789}

RBFSampler
    .. code-block:: python

       {'random_state': 123456789}

SkewedChi2Sampler
    .. code-block:: python

       {'random_state': 123456789}

.. _feature_hasher:

feature_hasher *(Optional)*
"""""""""""""""""""""""""""

If "true", this enables a high-speed, low-memory vectorizer that uses
feature hashing for converting feature dictionaries into NumPy arrays
instead of using a
`DictVectorizer <https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.DictVectorizer.html>`__.  This flag will drastically
reduce memory consumption for data sets with a large number of
features. If enabled, the user should also specify the number of
features in the :ref:`hasher_features <hasher_features>` field.  For additional
information see `the scikit-learn documentation <https://scikit-learn.org/stable/modules/feature_extraction.html#feature-hashing>`__.

.. _hasher_features:

hasher_features *(Optional)*
""""""""""""""""""""""""""""

The number of features used by the `FeatureHasher <https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.FeatureHasher.html>`__ if the
:ref:`feature_hasher <feature_hasher>` flag is enabled.

.. note::

    To avoid collisions, you should always use the power of two larger than the
    number of features in the data set for this setting. For example, if you
    had 17 features, you would want to set the flag to 32.

.. _featureset_names:

featureset_names *(Optional)*
"""""""""""""""""""""""""""""

Optional list of names for the feature sets.  If omitted, then the prefixes
will be munged together to make names.

.. _fixed_parameters:

fixed_parameters *(Optional)*
"""""""""""""""""""""""""""""

List of dicts containing parameters you want to have fixed for each
learner in :ref:`learners` list. Any empty ones will be ignored
(and the defaults will be used). If :ref:`grid_search` is ``True``,
there is a potential for conflict with specified/default parameter grids
and fixed parameters.

The default fixed parameters (beyond those that scikit-learn sets) are:

AdaBoostClassifier and AdaBoostRegressor
    .. code-block:: python

       {'n_estimators': 500, 'random_state': 123456789}

DecisionTreeClassifier and DecisionTreeRegressor
    .. code-block:: python

       {'random_state': 123456789}

DummyClassifier
    .. code-block:: python

       {'random_state': 123456789}

ElasticNet
    .. code-block:: python

       {'random_state': 123456789}

GradientBoostingClassifier and GradientBoostingRegressor
    .. code-block:: python

       {'n_estimators': 500, 'random_state': 123456789}

Lasso:
    .. code-block:: python

       {'random_state': 123456789}

LinearSVC and LinearSVR
    .. code-block:: python

       {'random_state': 123456789}

LogisticRegression
    .. code-block:: python

       {'random_state': 123456789}

MLPClassifier and MLPRegressor:
    .. code-block:: python

       {'learning_rate': 'invscaling', max_iter': 500}

RandomForestClassifier and RandomForestRegressor
    .. code-block:: python

       {'n_estimators': 500, 'random_state': 123456789}

RANSACRegressor
    .. code-block:: python

       {'loss': 'squared_loss', 'random_state': 123456789}

Ridge and RidgeClassifier
    .. code-block:: python

       {'random_state': 123456789}

SVC and SVR
    .. code-block:: python

       {'cache_size': 1000}

SGDClassifier
    .. code-block:: python

       {'loss': 'log', 'random_state': 123456789}

SGDRegressor
    .. code-block:: python

       {'random_state': 123456789}

TheilSenRegressor
    .. code-block:: python

       {'random_state': 123456789}


.. _imbalanced_data:

.. note::
    This option allows us to deal with imbalanced data sets by using
    the parameter ``class_weight`` for the classifiers:
    ``DecisionTreeClassifier``, ``LogisticRegression``,  ``LinearSVC``,
    ``RandomForestClassifier``, ``RidgeClassifier``, ``SGDClassifier``,
    and ``SVC``.

    Two possible options are available. The first one is ``balanced``,
    which automatically adjust weights inversely proportional to class
    frequencies, as shown in the following code:

    .. code-block:: python

       {'class_weight': 'balanced'}

    The second option allows you to assign a specific weight per each
    class. The default weight per class is 1. For example:

    .. code-block:: python

       {'class_weight': {1: 10}}

    Additional examples and information can be seen `here <https://scikit-learn.org/stable/auto_examples/linear_model/plot_sgd_weighted_samples.html>`__.

.. _feature_scaling:

feature_scaling *(Optional)*
""""""""""""""""""""""""""""

Whether to scale features by their mean and/or their standard deviation. If you
scale by mean, your data will automatically be converted to dense, so use
caution when you have a very large dataset. Valid options are:

none
    Perform no feature scaling at all.

with_std
    Scale feature values by their standard deviation.

with_mean
    Center features by subtracting their mean.

both
    Perform both centering and scaling.

Defaults to ``none``.

.. _tuning:

Tuning
^^^^^^

.. _grid_search:

grid_search *(Optional)*
""""""""""""""""""""""""

Whether or not to perform grid search to find optimal parameters for
classifier. Defaults to ``False``. Note that for the
:ref:`learning_curve <learning_curve>` task, grid search is not allowed
and setting it to ``True`` will generate a warning and be ignored.

.. _grid_search_folds:

grid_search_folds *(Optional)*
""""""""""""""""""""""""""""""

The number of folds to use for grid search. Defaults to 3.

.. _grid_search_jobs:

grid_search_jobs *(Optional)*
"""""""""""""""""""""""""""""

Number of folds to run in parallel when using grid search. Defaults to
number of grid search folds.

.. _use_folds_file_for_grid_search:

use_folds_file_for_grid_search *(Optional)*
"""""""""""""""""""""""""""""""""""""""""""

Whether to use the specified :ref:`folds_file <folds_file>` for the inner grid-search
cross-validation loop when :ref:`task` is set to ``cross_validate``.
Defaults to ``True``.

.. note::

    This flag is ignored for all other tasks, including the
    ``train`` task where a specified :ref:`folds_file <folds_file>` is
    *always* used for the grid search.

.. _min_feature_count:

min_feature_count *(Optional)*
""""""""""""""""""""""""""""""

The minimum number of examples for which the value of a feature must be nonzero
to be included in the model. Defaults to 1.

.. _objectives:

objectives *(Optional)*
"""""""""""""""""""""""

The objective functions to use for tuning. This is a list of one or more objective functions. Valid options are:

.. _classification_obj:

Classification:

    *   **accuracy**: Overall `accuracy <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html>`__
    *   **precision**: `Precision <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html>`__
    *   **recall**: `Recall <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html>`__
    *   **f1**: The default scikit-learn |F1 link|_
        (F\ :sub:`1` of the positive class for binary classification, or the weighted average F\ :sub:`1` for multiclass classification)
    *   **f1_score_micro**: Micro-averaged |F1 link|_
    *   **f1_score_macro**: Macro-averaged |F1 link|_
    *   **f1_score_weighted**: Weighted average |F1 link|_
    *   **f1_score_least_frequent**: F:\ :sub:`1` score of the least frequent
        class. The least frequent class may vary from fold to fold for certain
        data distributions.
    * **neg_log_loss**: The negative of the classification `log loss <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html>`__ . Since scikit-learn `recommends <https://scikit-learn.org/stable/modules/model_evaluation.html#common-cases-predefined-values>`__ using negated loss functions as scorer functions, SKLL does the same for the sake of consistency. To use this as the objective, :ref:`probability <probability>` must be set to ``True``.
    *   **average_precision**: `Area under PR curve <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html>`__
        (for binary classification)
    *   **roc_auc**: `Area under ROC curve <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html>`__
        (for binary classification)

.. |F1 link| replace:: F\ :sub:`1` score
.. _F1 link: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html

.. _int_label_classification_obj:

Regression or classification with integer labels:

    *   **unweighted_kappa**: Unweighted `Cohen's kappa <https://en.wikipedia.org/wiki/Cohen's_kappa>`__ (any floating point
        values are rounded to ints)
    *   **linear_weighted_kappa**: Linear weighted kappa (any floating
        point values are rounded to ints)
    *   **quadratic_weighted_kappa**: Quadratic weighted kappa (any
        floating point values are rounded to ints)
    *   **uwk_off_by_one**: Same as ``unweighted_kappa``, but all ranking
        differences are discounted by one. In other words, a ranking of
        1 and a ranking of 2 would be considered equal.
    *   **lwk_off_by_one**: Same as ``linear_weighted_kappa``, but all
        ranking differences are discounted by one.
    *   **qwk_off_by_one**: Same as ``quadratic_weighted_kappa``, but all
        ranking differences are discounted by one.

.. _binary_label_classification_obj:

Regression or classification with binary labels:

    *   **kendall_tau**: `Kendall's tau <https://en.wikipedia.org/wiki/Kendall_tau_rank_correlation_coefficient>`__
    *   **pearson**: `Pearson correlation <https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient>`__
    *   **spearman**: `Spearman rank-correlation <https://en.wikipedia.org/wiki/Spearman's_rank_correlation_coefficient>`__

.. _regression_obj:

Regression:

    *   **r2**: `R2 <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html>`__
    *   **neg_mean_squared_error**: The negative of the `mean squared error <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html>`__ regression loss. Since scikit-learn `recommends <https://scikit-learn.org/stable/modules/model_evaluation.html#common-cases-predefined-values>`__ using negated loss functions as scorer functions, SKLL does the same for the sake of consistency.


Defaults to ``['f1_score_micro']``.

.. note::
    1. Using ``objective=x`` instead of ``objectives=['x']`` is also acceptable, for backward-compatibility.
    2. Also see the :ref:`metrics <metrics>` option below.

.. _param_grids:

param_grids *(Optional)*
""""""""""""""""""""""""

List of parameter grids to search for each learner. Each parameter
grid should be a list of dictionaries mapping from strings to lists
of parameter values. When you specify an empty list for a learner,
the default parameter grid for that learner will be searched.

The default parameter grids for each learner are:

AdaBoostClassifier and AdaBoostRegressor
    .. code-block:: python

        [{'learning_rate': [0.01, 0.1, 1.0, 10.0, 100.0]}]

BayesianRidge
    .. code-block:: python

        [{'alpha_1': [1e-6, 1e-4, 1e-2, 1, 10],
          'alpha_2': [1e-6, 1e-4, 1e-2, 1, 10],
          'lambda_1': [1e-6, 1e-4, 1e-2, 1, 10],
          'lambda_2': [1e-6, 1e-4, 1e-2, 1, 10]}]

DecisionTreeClassifier and DecisionTreeRegressor
    .. code-block:: python

       [{'max_features': ["auto", None]}]

ElasticNet
    .. code-block:: python

       [{'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}]

GradientBoostingClassifier and GradientBoostingRegressor
    .. code-block:: python

       [{'max_depth': [1, 3, 5]}]

HuberRegressor
    .. code-block:: python

        [{'epsilon': [1.05, 1.35, 1.5, 2.0, 2.5, 5.0],
          'alpha': [1e-4, 1e-3, 1e-3, 1e-1, 1, 10, 100, 1000]}]

KNeighborsClassifier and KNeighborsRegressor
    .. code-block:: python

        [{'n_neighbors': [1, 5, 10, 100],
          'weights': ['uniform', 'distance']}]

Lasso
    .. code-block:: python

       [{'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}]

LinearSVC
    .. code-block:: python

       [{'C': [0.01, 0.1, 1.0, 10.0, 100.0]}]

LogisticRegression
    .. code-block:: python

       [{'C': [0.01, 0.1, 1.0, 10.0, 100.0]}]

MLPClassifier and MLPRegressor:
    .. code-block:: python

       [{'activation': ['logistic', 'tanh', 'relu'],
         'alpha': [1e-4, 1e-3, 1e-3, 1e-1, 1],
         'learning_rate_init': [0.001, 0.01, 0.1]}],

MultinomialNB
    .. code-block:: python

       [{'alpha': [0.1, 0.25, 0.5, 0.75, 1.0]}]

RandomForestClassifier and RandomForestRegressor
    .. code-block:: python

       [{'max_depth': [1, 5, 10, None]}]

Ridge and RidgeClassifier
    .. code-block:: python

       [{'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}]

SGDClassifier and SGDRegressor
    .. code-block:: python

        [{'alpha': [0.000001, 0.00001, 0.0001, 0.001, 0.01],
          'penalty': ['l1', 'l2', 'elasticnet']}]

SVC
    .. code-block:: python

       [{'C': [0.01, 0.1, 1.0, 10.0, 100.0],
         'gamma': ['auto', 0.01, 0.1, 1.0, 10.0, 100.0]}]

SVR
    .. code-block:: python

       [{'C': [0.01, 0.1, 1.0, 10.0, 100.0]}]


.. note::
    Note that learners not listed here do not have any default
    parameter grids in SKLL either because either there are no
    hyper-parameters to tune or decisions about which parameters
    to tune (and how) depend on the data being used for the
    experiment and are best left up to the user.


.. _pos_label_str:

pos_label_str *(Optional)*
""""""""""""""""""""""""""

The string label for the positive class in the binary
classification setting. If unspecified, an arbitrary class is
picked.

.. _output:

Output
^^^^^^

.. _probability:

probability *(Optional)*
""""""""""""""""""""""""

Whether or not to output probabilities for each class instead of the
most probable class for each instance. Only really makes a difference
when storing predictions. Defaults to ``False``. Note that this also
applies to the tuning objective.

.. _results:

results *(Optional)*
""""""""""""""""""""

Directory to store result files in. If omitted, the current working
directory is used.

.. _metrics:

metrics *(Optional)*
""""""""""""""""""""
For the ``evaluate`` and ``cross_validate`` tasks, this is a list of
additional metrics that will be computed *in addition to* the tuning
objectives and added to the results files. For the ``learning_curve`` task,
this will be the list of metrics for which the learning curves
will be plotted. Can take all of the same functions as those
available for the :ref:`tuning objectives <objectives>`.

.. note::

    1. For learning curves, ``metrics`` can be specified instead of
       ``objectives`` since both serve the same purpose. If both are
       specified, ``objectives`` will be ignored.
    2. For the ``evaluate`` and ``cross_validate`` tasks,  any functions
       that are specified in both ``metrics`` and  ``objectives``
       are assumed to be the latter.
    3. If you just want to use ``neg_log_loss`` as an additional metric,
       you do not need to set :ref:`probability <probability>` to ``True``.
       That's only neeeded for ``neg_log_loss`` to be used as a tuning
       objective.

.. _log:

log *(Optional)*
""""""""""""""""

Directory to store log files in. If omitted, the current working
directory is used.

.. _models:

models *(Optional)*
"""""""""""""""""""

Directory to store trained models in. Can be omitted to not store
models.

.. _predictions:

predictions *(Optional)*
""""""""""""""""""""""""

Directory to store prediction files in. Can be omitted to not store
predictions.

.. note::

    You can use the same directory for :ref:`results <results>`,
    :ref:`log <log>`, :ref:`models <models>`, and
    :ref:`predictions <predictions>`.


.. _save_cv_folds:

save_cv_folds *(Optional)*
""""""""""""""""""""""""""

Whether to save the folds that were used for a cross-validation experiment
to a CSV file named ``EXPERIMENT_skll_fold_ids.csv`` in the :ref:`results`
directory, where ``EXPERIMENT`` refers to the :ref:`experiment_name`.
Defaults to ``False``.

.. _run_experiment:

Using run_experiment
--------------------
.. program:: run_experiment

Once you have created the :ref:`configuration file <create_config>` for your
experiment, you can usually just get your experiment started by running
``run_experiment CONFIGFILE``. [#]_ That said, there are a few options that are
specified via command-line arguments instead of in the configuration file:

.. option:: -a <num_features>, --ablation <num_features>

    Runs an ablation study where repeated experiments are conducted with the
    specified number of feature files in each featureset in the
    configuration file held out. For example, if you have three feature
    files (``A``, ``B``, and ``C``) in your featureset and you specifiy
    ``--ablation 1``, there will be three experiments conducted with
    the following featuresets: ``[[A, B], [B, C], [A, C]]``. Additionally,
    since every ablation experiment includes a run with all the features as a
    baseline, the following featureset will also be run: ``[[A, B, C]]``.

    If you would like to try all possible combinations of feature files, you
    can use the :option:`run_experiment --ablation_all` option instead.

    .. warning::

        Ablation will *not* work if you specify a :ref:`train_file <train_file>`
        and :ref:`test_file <test_file>` since no featuresets are defined in
        that scenario.

.. option:: -A, --ablation_all

    Runs an ablation study where repeated experiments are conducted with all
    combinations of feature files in each featureset.

    .. warning::

        This can create a huge number of jobs, so please use with caution.

.. option:: -k, --keep-models

    If trained models already exist for any of the learner/featureset
    combinations in your configuration file, just load those models and
    do not retrain/overwrite them.

.. option:: -r, --resume

    If result files already exist for an experiment, do not overwrite them.
    This is very useful when doing a large ablation experiment and part of
    it crashes.

.. option:: -v, --verbose

    Print more status information. For every additional time this flag is
    specified, output gets more verbose.

.. option:: --version

    Show program's version number and exit.

GridMap options
^^^^^^^^^^^^^^^

If you have `GridMap <https://pypi.org/project/gridmap/>`__ installed,
:program:`run_experiment` will automatically schedule jobs on your DRMAA-
compatible cluster. You can use the following options to customize this
behavior.

.. option:: -l, --local

    Run jobs locally instead of using the cluster. [#]_

.. option:: -q <queue>, --queue <queue>

    Use this queue for `GridMap <https://pypi.org/project/gridmap/>`__.
    (default: ``all.q``)

.. option:: -m <machines>, --machines <machines>

    Comma-separated list of machines to add to GridMap's whitelist.  If not
    specified, all available machines are used.

    .. note::

        Full names must be specified, (e.g., ``nlp.research.ets.org``).


Output files
^^^^^^^^^^^^

For most of the tasks, the result, log, model, and prediction files generated by
``run_experiment`` will all share the automatically generated prefix
``EXPERIMENT_FEATURESET_LEARNER_OBJECTIVE``, where the following definitions hold:

    ``EXPERIMENT``
        The name specified as :ref:`experiment_name` in the configuration file.

    ``FEATURESET``
        The feature set we're training on joined with "+".

    ``LEARNER``
        The learner the current results/model/etc. was generated using.

    ``OBJECTIVE``
        The objective function the current results/model/etc. was generated using.

However, if ``objectives`` contains only one objective function,
the result, log, model, and prediction files will share the prefix
``EXPERIMENT_FEATURESET_LEARNER``. For backward-compatibility, the same
applies when a single objective is specified using ``objective=x``.

In addition to the above log files that are specific to each "job"
(a specific combination of featuresets, learners, and objectives specified
in the configuration file), SKLL also produces a single, top level "experiment"
log file with only ``EXPERIMENT`` as the prefix. While the job-level log files
contain messages that pertain to the specific characteristics of the job, the
experiment-level log file will contain logging messages that pertain to the
overall experiment and configuration file. The messages in the log files are
in the following format:

.. code-block:: bash

    TIMESTAMP - LEVEL - MSG

where ``TIMESTAMP`` refers to the exact time when the message was logged,
``LEVEL`` refers to the level of the logging message (e.g., ``INFO``, ``WARNING``,
etc.), and ``MSG`` is the actual content of the message. All of the messages
are also printed to the console in addition to being saved in the job-level log
files and the experiment-level log file.

For every experiment you run, there will also be a result summary file
generated that is a tab-delimited file summarizing the results for each
learner-featureset combination you have in your configuration file. It is named
``EXPERIMENT_summary.tsv``. For :ref:`learning_curve <learning_curve>`
experiments, this summary file will contain training set sizes and the averaged
scores for all combinations of featuresets, learners, and objectives.

If `pandas <http://pandas.pydata.org>`__ and `seaborn <http://seaborn.pydata.org>`__
are available when running a :ref:`learning_curve <learning_curve>` experiment,
actual learning curves are also generated as PNG files - one for each feature set
specified in the configuration file. Each PNG file is named ``EXPERIMENT_FEATURESET.png``
and contains a faceted learning curve plot for the featureset with objective
functions on rows and learners on columns. Here's an example of such a plot.

If you didn't have pandas and seaborn available when running the learning curve
experiment, you can always generate the plots later from the learning curve summary
file using the :ref:`plot_learning_curves <plot_learning_curves>` utility script.

    .. image:: learning_curve.png


.. rubric:: Footnotes

.. [#] We are considering adding support for YAML configuration files in the
   future, but we have not added this functionality yet.
.. [#] K-1 folds will be used for grid search within CV, so there should be at
   least 3 fold IDs.
.. [#] If you installed SKLL via pip on macOS, you might get an error when
   using ``run_experiment`` to generate learning curves. To get around this,
   add ``MPLBACKEND=Agg`` before the ``run_experiment`` command and re-run.
.. [#] This will happen automatically if GridMap cannot be imported.
