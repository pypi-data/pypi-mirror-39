Using the conversion scripts
============================

Two main types of data can be converted with these scripts: image volumes, and
surface meshes.

Converting image volumes
------------------------

Here is a summary of the steps needed for converting volumetric images to the
Neuroglancer precomputed chunk format.

Two types of data layout are accepted as input:

- Volumes in NIfTI format (or any other format readable by Nibabel). See
  :ref:`JuBrain` for an example.

- Series of 2D slices. See :ref:`BigBrain` for an example.


1. Write the metadata for the full-resolution image `in JSON format
   <https://github.com/google/neuroglancer/blob/master/src/neuroglancer/datasource/precomputed/README.md>`_.
   If your input data is readable by Nibabel, you can use
   ``volume-to-precomputed --generate-info`` do do the job. Here is an example
   with minimal metadata (note that the resolution is expressed in
   *nanometres*):

   .. code-block:: json

     {
       "type": "image",
       "data_type": "uint8",
       "num_channels": 1,
       "scales": [
         {
           "size": [151, 188, 154],
           "resolution": [1000000, 1000000, 1000000],
           "voxel_offset": [0, 0, 0]
         }
       ]
     }

2. Create metadata for all scales using ``generate-scales-info`` on the
   previously created JSON file. This step writes a file named ``info`` in the
   current directory, which is needed by Neuroglancer as well as by all the
   subsequent steps. You are advised to create a fresh directory for each
   dataset.

   You can use any lossless encoding for the following steps (i.e. ``raw`` or
   ``compressed_segmentation``).

   At this stage you may want to run ``scale-stats``, which displays the
   number of chunks that will be created, and their uncompressed size. Thus,
   you can make sure that you have enough disk space before proceeding.

3. Convert your data to raw full-resolution chunks by using one of these
   scripts:
   - ``slices-to-precomputed``
   - ``volume-to-precomputed``

4. Compute downscaled pyramid levels using ``compute-scales``. Make sure to
   use the correct downscaling method (``average`` for greyscale images,
   ``majority`` for segmentations, or ``stride`` for a fast low-quality
   downsampling).

   At this point the raw-format data is ready to be displayed in Neuroglancer.

5. Optionally, you can convert the raw chunks to a compressed format using
   ``convert-chunks``. You will need to generate these compressed chunks in
   a separate directory from the raw chunks, and generate a suitable *info*
   file by using the ``--encoding`` parameter to ``generate-scales-info``.
   Two compressed encodings are available:

   - ``compressed_segmentation``: lossless compression, recommended for images
     containing discrete labels;

   - ``jpeg``: lossy JPEG compression, see ``--jpeg-quality`` and ``--jpeg-plane``.


Converting surface meshes
-------------------------

A surface mesh can be displayed in two ways in Neuroglancer: associated with a
segmentation label as part of a ``segmentation`` type layer, or as a standalone
mesh layer.

A mesh associated with a segmentation label needs to be in a
Neuroglancer-specific binary precomputed format. ``mesh-to-precomputed`` can be
used to convert meshes to this format. The ``link-mesh-fragments`` command must
then be used so that Neuroglancer knows what meshes are associated to each
label of the segmentation. See the last step of :ref:`BigBrain` for an example.
