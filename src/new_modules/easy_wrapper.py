# higher level wrapper
def write_to_database(p):
    gen = emit_flat_data(p)
    stream_to_database(gen)
