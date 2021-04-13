import vcfpy

def parseVCF():

    # Open file, this will read in the header
    reader = vcfpy.Reader.from_path('variants.vcf')

    # Build and print header
    # header = reader.header.samples.names
    # print('\t'.join(header))

    for record in reader:
        if not record.is_snv():
            continue
        line = [call.data.get('GT') or './.' for call in record.calls]
        print('\t'.join(map(str, line)))



parseVCF()
