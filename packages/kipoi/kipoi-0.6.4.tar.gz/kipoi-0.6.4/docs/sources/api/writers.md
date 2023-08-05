#kipoi.writers

Writers used in `kipoi predict`

- TsvBatchWriter
- BedBatchWriter
- HDF5BatchWriter
- RegionWriter
- BedGraphWriter
- BigWigWriter

##TsvBatchWriter

```python
TsvBatchWriter(self, file_path, nested_sep='/')
```
Tab-separated file writer

__Arguments__

- __file_path (str)__: File path of the output tsv file
- __nested_sep__: What separator to use for flattening the nested dictionary structure
    into a single key

###batch_write

```python
TsvBatchWriter.batch_write(self, batch)
```
Write a batch of data

__Arguments__

- __batch__: batch of data. Either a single `np.array` or a list/dict thereof.

##BedBatchWriter

```python
BedBatchWriter(self, file_path, metadata_schema, header=True)
```
Bed-file writer

__Arguments__

- __file_path (str)__: File path of the output tsv file
- __dataloader_schema__: Schema of the dataloader. Used to find the ranges object
- __nested_sep__: What separator to use for flattening the nested dictionary structure
    into a single key

###batch_write

```python
BedBatchWriter.batch_write(self, batch)
```
Write a batch of data to bed file

__Arguments__

- __batch__: batch of data. Either a single `np.array` or a list/dict thereof.

##HDF5BatchWriter

```python
HDF5BatchWriter(self, file_path, chunk_size=10000, compression='gzip')
```
HDF5 file writer

__Arguments__

- __file_path (str)__: File path of the output tsv file
- __chunk_size (str)__: Chunk size for storing the files
- __nested_sep__: What separator to use for flattening the nested dictionary structure
    into a single key
- __compression (str)__: default compression to use for the hdf5 datasets.
- __see also__: <http://docs.h5py.org/en/latest/high/dataset.html#dataset-compression>

###batch_write

```python
HDF5BatchWriter.batch_write(self, batch)
```
Write a batch of data to bed file

__Arguments__

- __batch__: batch of data. Either a single `np.array` or a list/dict thereof.

###close

```python
HDF5BatchWriter.close(self)
```
Close the file handle

###dump

```python
HDF5BatchWriter.dump(file_path, batch)
```
In a single shot write the batch/data to a file and
close the file.

__Arguments__

- __file_path__: file path
- __batch__: batch of data. Either a single `np.array` or a list/dict thereof.

##BedGraphWriter

```python
BedGraphWriter(self, file_path)
```

__Arguments__

- __file_path (str)__: File path of the output bedgraph file

###region_write

```python
BedGraphWriter.region_write(self, region, data)
```
Write region to file.

__Arguments__

- __region__: Defines the region that will be written position by position. Example: `{"chr":"chr1", "start":0, "end":4}`.
- __data__: a 1D or 2D numpy array vector that has length "end" - "start". if 2D array is passed then
        `data.sum(axis=1)` is performed on it first.

###write_entry

```python
BedGraphWriter.write_entry(self, chr, start, end, value)
```
Write region to file.

__Arguments__

- __region__: Defines the region that will be written position by position. Example: `{"chr":"chr1", "start":0, "end":4}`.
- __data__: a 1D or 2D numpy array vector that has length "end" - "start". if 2D array is passed then
        `data.sum(axis=1)` is performed on it first.

###close

```python
BedGraphWriter.close(self)
```
Close the file

##BigWigWriter

```python
BigWigWriter(self, file_path)
```
BigWig entries have to be sorted so the generated values are cached in a bedgraph file.

__Arguments__

- __file_path (str)__: File path of the output tsv file

###write_entry

```python
BigWigWriter.write_entry(self, chr, start, end, value)
```
Write region to file.

__Arguments__

- __region__: Defines the region that will be written position by position. Example: `{"chr":"chr1", "start":0, "end":4}`.
- __data__: a 1D or 2D numpy array vector that has length "end" - "start". if 2D array is passed then
        `data.sum(axis=1)` is performed on it first.

###close

```python
BigWigWriter.close(self)
```
Close the file

