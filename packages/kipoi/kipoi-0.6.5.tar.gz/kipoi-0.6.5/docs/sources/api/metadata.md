#kipoi.metadata

Module defining different metadata classes compatible with dataloaders

All classes inherit from `collections.Mapping` which allows to use
`kipoi.data_utils.numpy_collate` on them (e.g. they behave as a dictionary).

##GenomicRanges

```python
GenomicRanges(self, chr, start, end, id, strand='*')
```
Container for genomic interval(s)

All fields can be either a single values (str or int) or a
numpy array of values.

__Arguments__

- __chr (str or np.array)__: Chromosome(s)
- __start (int or np.array)__: Interval start (0-based coordinates)
- __end (int or np.array)__: Interval end (0-based coordinates)
- __id (str or np.array)__: Interval id
- __strand (str or np.array)__: Interval strand ("+", "-", or "*")

###from_interval

```python
GenomicRanges.from_interval(interval)
```
Create the ranges object from `pybedtools.Interval`

__Arguments__

- __interval__: `pybedtools.Interval` instance

###to_interval

```python
GenomicRanges.to_interval(self)
```
Convert GenomicRanges object to a Interval object

__Returns__

    (pybedtools.Interval or list[pybedtools.Interval])

