from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import warnings

import numpy as np
import pandas as pd

from .data import COGS

class AnnotationTable:
    def __init__(self, source=None):

        if source is None:
            source = pd.DataFrame()

        if type(source) == pd.core.frame.DataFrame:
            self.data = source

        elif type(source) == str:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                df = pd.read_table(
                    source,
                    comment="#",
                    sep="\t",
                    na_values=["."],
                    names=["seqid", "source", "type", "start", "end", "score", "strand",
                          "phase", "attributes"])

            # remove FASTA from bottom of file and reset types
            df = df[pd.notna(df["strand"])]
            for col_name in ["start", "end"]:
                df[col_name] = df[col_name].astype(np.int)

            # calculate length
            df["length"] = (df["start"] - df["end"]).abs()

            # expand attributes
            attribute_cols = set()
            for attributes in df["attributes"]:
                matches = re.findall("([^=;]+)=[^;]+", attributes)
                attribute_cols.update(matches)

            for col in attribute_cols:
                df[col] = df["attributes"].str.extract("%s=([^;]+)" % col)

            # get prokka-specific features from attributes
            df["uniprot_match"] = df["inference"].str.extract("UniProtKB:([\w]+)")
            df["COG"] = df["dbxref"].str.extract("COG:(COG\d{4})")

            # drop columns where all values are null
            df.dropna(how='all', axis=1)

            self.data = df
            self.columns = list(df)
        else:
            raise ValueError("AnnotationTable accepts either a string (path to a gff) or a pandas dataframe")

    def as_df(self):
        return self.data

    def get(self, field, value):
        # handle case where value is a function
        if callable(value):
            return AnnotationTable(self.data[self.data[field].apply(value)])

        # handle case where exact value is given
        else:
            return AnnotationTable(self.data[self.data[field] == value])

    def append(self, annotation_table):
        return AnnotationTable(self.data.append(annotation_table.data))

    def compare(self, other, field):
        shared_values = self.data[field][self.data[field].isin(other.data[field])].drop_duplicates()
        only_in_self = self.data[field][~self.data[field].isin(other.data[field])].drop_duplicates()
        only_in_other = other.data[field][~other.data[field].isin(self.data[field])].drop_duplicates()

        return {"shared": shared_values, "unique": only_in_other, "missing": only_in_self}

    # TODO: delete
    # def compare_counts(self, other, field):
    #     counts = pd.DataFrame({"original": self.data[field].value_counts(),
    #         "comparison": other.data[field].value_counts()}).fillna(0)
    #
    #     counts = counts[counts["original"] != counts["comparison"]]
    #     counts["difference"] = (counts["original"] - counts["comparison"]).abs()
    #
    #     return counts.sort_values("difference", ascending=False)

# TODO: implement
# def count_against_references(target, references, field):
#     target_data = target.data[field].drop_duplicates()
#     matches = pd.Series(np.zeros(len(target_data)))
#
#     for organism in references:
#         target_data.isin(references[organism].data[field]).astype(int)

def compare_counts(annotations, field):
    assert len(annotations) >= 2
    counts = pd.DataFrame({key: value.data[field].value_counts() for (key, value) in annotations.items()}).fillna(0).astype(np.int)
    organisms = list(annotations.keys())
    equal = counts[organisms[0]] == counts[organisms[1]]
    for organism in organisms[2:]:
        equal &= counts[organisms[0]] == counts[organism]

    counts = counts[~equal]
    counts["difference"] = counts.max(axis=1) - counts.min(axis=1)
    return counts.sort_values("difference", ascending=False)

def compare_cogs(annotations):
    cog_counts = compare_counts(annotations, "COG")
    cog_counts["category"] = [COGS.loc[cog]["function"] for cog in cog_counts.index]
    cog_counts["name"] = [COGS.loc[cog]["name"] for cog in cog_counts.index]
    return cog_counts
