0.1.52 (2018-12-03)
-----------------------

- Fixed bug in :py:func:`~cosmo_utils.utils.web_utils.url_files_download` again.

0.1.51 (2018-12-03)
-----------------------

- Fixed bug in :py:func:`~cosmo_utils.utils.web_utils.url_files_download`

0.1.50 (2018-12-03)
-----------------------

- Added :py:func:`~cosmo_utils.utils.web_utils.url_file_list` and
  :py:func:`~cosmo_utils.utils.web_utils.url_files_download` to utilities.

0.1.48 (2018-11-24)
-----------------------

- Fixed bugs

0.1.47 (2018-11-24)
-----------------------

- Fixed bug in :py:func:`~cosmo_utils.utils.stats_funcs.Stats_one_arr`.

0.1.46 (2018-10-04)
-----------------------

- Updated function :py:class:`~cosmo_utils.mock_catalogues.hod_funcs.HOD` to accomodate for better use.

0.1.45 (2018-10-03)
-----------------------

- Added new class for determining average number of galaxies as function
  of logarithmic halo mass :py:class:`~cosmo_utils.mock_catalogues.hod_funcs.HOD`

0.1.44 (2018-09-19)
-----------------------

- New function :py:func:`~cosmo_utils.utils.gen_utils.array_insert`.
- Updated function :py:func:`~cosmo_utils.mock_catalogues.shmr_funcs.Behroozi_relation`
  and fixed bug.

0.1.43 (2018-06-02)
-----------------------

- Fixed another bug in
  :py:func:`~cosmo_utils.ml.ml_utils.scoring_methods` with the `None` type.

0.1.42 (2018-06-02)
-----------------------

- Fixed bug with `feat_arr` in 
  :py:func:`~cosmo_utils.ml.ml_utils.scoring_methods`

0.1.41 (2018-05-31)
-----------------------

- Added module :py:module:`~cosmo_utils.utils.gen_utils`
- Expanded functionality in :py:func:`~cosmo_utils.ml.ml_utils.data_preprocessing`
  and :py:func:`~cosmo_utils.ml.ml_utils.train_test_dataset`.

0.1.40 (2018-05-30)
-----------------------

- Fixed bugs in :py:func:`~cosmo_utils.ml.ml_utils.train_test_dataset`

0.1.39 (2018-05-30)
-----------------------

- Used Flake8 Lint to go over the style of the code, and fixed bugs along the way

0.1.38 (2018-05-30)
-----------------------

- Fixed bug found in :py:func:`~cosmo_utils.utils.file_readers.pandas_df_to_hdf5_file`

0.1.37 (2018-05-29)
-----------------------

- Changed range for `hod_n_valid` in :py:func:`~cosmo_utils.mock_catalogues.catls_utils.catl_sdss_merge`
  , :py:func:`~cosmo_utils.mock_catalogues.catls_utils.catl_sdss_dir` and 
  , :py:func:`~cosmo_utils.mock_catalogues.catls_utils.extract_catls`.

0.1.36 (2018-05-27)
-----------------------

- A change in the path in 
  :py:func:`~cosmo_utils.utils.work_paths.get_sdss_catl_dir` and
  :py:func:`~cosmo_utils.utils.work_paths.get_output_path`

0.1.35 (2018-05-27)
-----------------------

- Fixed issue with path in 
  :py:func:`~cosmo_utils.mock_catalogues.catls_utils.catl_sdss_merge`

0.1.32 (2018-05-27)
-----------------------

- Modified paths in :py:func:`~cosmo_utils.utils.work_paths.cookiecutter_paths`
- Fixed path in :py:func:`~cosmo_utils.mock_catalogues.catls_utils.catl_sdss_merge`.

0.1.31 (2018-05-26)
-----------------------

- Added path and more for *velocity bias*

0.1.30 (2018-05-23)
-----------------------

- Minor bug in :py:func:`~cosmo_utils.utils.file_utils.mark_parametrize` fixed.

0.1.29 (2018-05-23)
-----------------------

- Added decorator to loop over different set of values (:py:func:`~cosmo_utils.utils.file_utils.mark_parametrize`).
- Fixed docstrings.

0.1.28 (2018-05-21)
-----------------------

- Fixed bug with :py:func:`~cosmo_utils.utils.file_utils.Path_Folder`

0.1.27 (2018-05-21)
-----------------------

- Modified the modules imported in :py:func:`~cosmo_utils.mock_catalogues.spherematch.spherematch`

0.1.26 (2018-05-17)
-----------------------

- Added some useful functions related to machine learning.
- Fixed bugs in testing.

0.1.25 (2018-05-17)
-----------------------

- Introduced `pairwise` counting again.
- Fixed bug in :py:func:`~cosmo_utils.mock_catalogues.shmr_funcs.Behroozi_relation`

0.1.24 (2018-05-17)
-----------------------

- Importing modules in a different way
- Temporarily disabled the function for `pairwise` counting.

0.1.23 (2018-05-16)
-----------------------

- Checking for input parameters (:py:func:`~cosmo_utils.utils.stats_funcs.sigma_calcs`)
- Fixed issue with galaxy type (:py:func:`~cosmo_utils.mock_catalogues.catls_utils.sdss_catl_clean_nmin`)

0.1.22 (2018-05-15)
-----------------------

- Fixed bug with function :py:func:`~cosmo_utils.mock_catalogues.catls_utils.sdss_catl_clean`

0.1.21 (2018-05-11)
-----------------------

- Initial release

