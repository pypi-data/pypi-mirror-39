#!/usr/bin/python


import sys

sys.dont_write_bytecode = True

def FastqGeneralIterator(handle):
    """Iterate over Fastq records as string tuples (not as SeqRecord objects).

    This code does not try to interpret the quality string numerically.  It
    just returns tuples of the title, sequence and quality as strings.  For
    the sequence and quality, any whitespace (such as new lines) is removed.

    Our SeqRecord based FASTQ iterators call this function internally, and then
    turn the strings into a SeqRecord objects, mapping the quality string into
    a list of numerical scores.  If you want to do a custom quality mapping,
    then you might consider calling this function directly.

    For parsing FASTQ files, the title string from the "@" line at the start
    of each record can optionally be omitted on the "+" lines.  If it is
    repeated, it must be identical.

    The sequence string and the quality string can optionally be split over
    multiple lines, although several sources discourage this.  In comparison,
    for the FASTA file format line breaks between 60 and 80 characters are
    the norm.

    **WARNING** - Because the "@" character can appear in the quality string,
    this can cause problems as this is also the marker for the start of
    a new sequence.  In fact, the "+" sign can also appear as well.  Some
    sources recommended having no line breaks in the  quality to avoid this,
    but even that is not enough, consider this example::

        @071113_EAS56_0053:1:1:998:236
        TTTCTTGCCCCCATAGACTGAGACCTTCCCTAAATA
        +071113_EAS56_0053:1:1:998:236
        IIIIIIIIIIIIIIIIIIIIIIIIIIIIICII+III
        @071113_EAS56_0053:1:1:182:712
        ACCCAGCTAATTTTTGTATTTTTGTTAGAGACAGTG
        +
        @IIIIIIIIIIIIIIICDIIIII<%<6&-*).(*%+
        @071113_EAS56_0053:1:1:153:10
        TGTTCTGAAGGAAGGTGTGCGTGCGTGTGTGTGTGT
        +
        IIIIIIIIIIIICIIGIIIII>IAIIIE65I=II:6
        @071113_EAS56_0053:1:3:990:501
        TGGGAGGTTTTATGTGGA
        AAGCAGCAATGTACAAGA
        +
        IIIIIII.IIIIII1@44
        @-7.%<&+/$/%4(++(%

    This is four PHRED encoded FASTQ entries originally from an NCBI source
    (given the read length of 36, these are probably Solexa Illumina reads where
    the quality has been mapped onto the PHRED values).

    This example has been edited to illustrate some of the nasty things allowed
    in the FASTQ format.  Firstly, on the "+" lines most but not all of the
    (redundant) identifiers are omitted.  In real files it is likely that all or
    none of these extra identifiers will be present.

    Secondly, while the first three sequences have been shown without line
    breaks, the last has been split over multiple lines.  In real files any line
    breaks are likely to be consistent.

    Thirdly, some of the quality string lines start with an "@" character.  For
    the second record this is unavoidable.  However for the fourth sequence this
    only happens because its quality string is split over two lines.  A naive
    parser could wrongly treat any line starting with an "@" as the beginning of
    a new sequence!  This code copes with this possible ambiguity by keeping
    track of the length of the sequence which gives the expected length of the
    quality string.

    Using this tricky example file as input, this short bit of code demonstrates
    what this parsing function would return:

    >>> with open("Quality/tricky.fastq", "rU") as handle:
    ...     for (title, sequence, quality) in FastqGeneralIterator(handle):
    ...         print(title)
    ...         print("%s %s" % (sequence, quality))
    ...
    071113_EAS56_0053:1:1:998:236
    TTTCTTGCCCCCATAGACTGAGACCTTCCCTAAATA IIIIIIIIIIIIIIIIIIIIIIIIIIIIICII+III
    071113_EAS56_0053:1:1:182:712
    ACCCAGCTAATTTTTGTATTTTTGTTAGAGACAGTG @IIIIIIIIIIIIIIICDIIIII<%<6&-*).(*%+
    071113_EAS56_0053:1:1:153:10
    TGTTCTGAAGGAAGGTGTGCGTGCGTGTGTGTGTGT IIIIIIIIIIIICIIGIIIII>IAIIIE65I=II:6
    071113_EAS56_0053:1:3:990:501
    TGGGAGGTTTTATGTGGAAAGCAGCAATGTACAAGA IIIIIII.IIIIII1@44@-7.%<&+/$/%4(++(%

    Finally we note that some sources state that the quality string should
    start with "!" (which using the PHRED mapping means the first letter always
    has a quality score of zero).  This rather restrictive rule is not widely
    observed, so is therefore ignored here.  One plus point about this "!" rule
    is that (provided there are no line breaks in the quality sequence) it
    would prevent the above problem with the "@" character.
    """
    # We need to call handle.readline() at least four times per record,
    # so we'll save a property look up each time:
    handle_readline = handle.readline

    # Skip any text before the first record (e.g. blank lines, comments?)
    while True:
        line = handle_readline()
        if not line:
            return  # Premature end of file, or just empty?
        if line[0] == "@":
            break
        if isinstance(line[0], int):
            raise ValueError("Is this handle in binary mode not text mode?")

    while line:
        if line[0] != "@":
            raise ValueError(
                "Records in Fastq files should start with '@' character")
        title_line = line[1:].rstrip()
        # Will now be at least one line of quality data - in most FASTQ files
        # just one line! We therefore use string concatenation (if needed)
        # rather using than the "".join(...) trick just in case it is multiline:
        seq_string = handle_readline().rstrip()
        # There may now be more sequence lines, or the "+" quality marker line:
        while True:
            line = handle_readline()
            if not line:
                raise ValueError("End of file without quality information.")
            if line[0] == "+":
                # The title here is optional, but if present must match!
                second_title = line[1:].rstrip()
                if second_title and second_title != title_line:
                    raise ValueError("Sequence and quality captions differ.")
                break
            seq_string += line.rstrip()  # removes trailing newlines
        # This is going to slow things down a little, but assuming
        # this isn't allowed we should try and catch it here:
        if " " in seq_string or "\t" in seq_string:
            raise ValueError("Whitespace is not allowed in the sequence.")
        seq_len = len(seq_string)

        # Will now be at least one line of quality data...
        quality_string = handle_readline().rstrip()
        # There may now be more quality data, or another sequence, or EOF
        while True:
            line = handle_readline()
            if not line:
                break  # end of file
            if line[0] == "@":
                # This COULD be the start of a new sequence. However, it MAY just
                # be a line of quality data which starts with a "@" character.  We
                # should be able to check this by looking at the sequence length
                # and the amount of quality data found so far.
                if len(quality_string) >= seq_len:
                    # We expect it to be equal if this is the start of a new record.
                    # If the quality data is longer, we'll raise an error below.
                    break
                # Continue - its just some (more) quality data.
            quality_string += line.rstrip()

        if seq_len != len(quality_string):
            raise ValueError("Lengths of sequence and quality values differs "
                             " for %s (%i and %i)."
                             % (title_line, seq_len, len(quality_string)))

        # Return the record and then continue...
        yield (title_line, seq_string, quality_string)
    raise StopIteration
