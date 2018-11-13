import hashlib
import os
import tempfile

import pysam

import bamreducers


def md5sum(filename):
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def test_input() -> pysam.AlignmentFile:
    return pysam.AlignmentFile(
        os.path.join(os.path.dirname(__file__), 'testfile.bam'))


def tmp_out(tmpname: str, template: pysam.AlignmentFile) -> pysam.AlignmentFile:
    return pysam.AlignmentFile(tmpname, 'wb', template=template)


def filter_result(filter: object) -> object:
    """ return the md5 digest of the result of running a filter"""
    with test_input() as tmpin:
        with tempfile.NamedTemporaryFile(delete=False) as tmpout:
            bamreducers.BamReducer([filter]).filter_bam(tmpin, tmpout.name)
    result = md5sum(tmpout.name)
    os.unlink(tmpout.name)
    return result


if __name__ == '__main__':
    print("tagstripper:", filter_result(bamreducers.BamTagStripper()))
    print("downsampler:", filter_result(bamreducers.BamDownSampler(5, seed=111)))
    print("sjvalidator:", filter_result(bamreducers.SJValidator()))
    print("qualremover:", filter_result(bamreducers.BamQualityRemover()))

