# Collections folder

All the input test collections are stored here. Each test collection has three files with the same name, but with extensions `.ALL`, `QRY`, and `REL`. The format of each file is described below.

### Fields in the `.ALL` and `.QRY` files

| Field | Meaning | Required? | Can be repeated? |
|---|---|---|---|
| ID (`.I`) | Document/Query **identifier** | Yes | No |
| Content (`.W`) | Document or query text | Yes | No |


### The `.REL` file

This is a `TSV` file with two columns:

| Column | Meaning | Meaning | Constraints |
|---|---|---|---|
| 1st | Query ID | Unique ID | Must correspond to a query in `.QRY` |
| 2nd | Document ID |ID of a relevant document | Must correspond to a document in `.ALL`|


## Original documentation about the CISI collection

The documentation below is from the authors, as described by them on Kaggle: https://www.kaggle.com/datasets/dmaso01dsta/cisi-a-dataset-for-information-retrieval
The collection (`CISI_simplified`) has been simplified to remove unused fields from the above data source.

# Checksums

```
MD5 (CISI_simplified.ALL) = 8da4909b75f9ca88531e1d6e6a0a76f6
MD5 (CISI_simplified.QRY) = b7eca0602e510ae3513428db80dcf876
MD5 (CISI_simplified.REL) = 66191983b1815ea6b61b9773684ed405
```

https://www.google.com/search?q=how+do+i+check+md5+checksum+command+line

