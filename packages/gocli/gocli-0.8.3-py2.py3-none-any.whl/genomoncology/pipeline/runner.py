from cytoolz.curried import do, pipe, map
from .sinks import Sink, JsonlFileSink
from .sources import Source, JsonlFileSource
from genomoncology.parse.ensures import flatten


def run_pipeline(processors, input, output):

    funcs, sinks = prep_funcs_sinks(processors, output)

    for _ in pipe(input, *funcs):
        pass

    for sink in sinks:
        sink.close()


def prep_funcs_sinks(processors, output):
    processors = flatten(processors)

    if not processors or not Source.is_source_class(processors[0]):
        processors.insert(0, JsonlFileSource)

    sinks = []
    funcs = []

    def add_sink(cls):
        sink = cls(output)
        sinks.append(sink)
        funcs.append(map(do(sink.write)))

    for processor in processors:
        if Sink.is_sink_class(processor):
            add_sink(processor)

        else:
            funcs.append(processor)

    if not sinks:
        add_sink(JsonlFileSink)

    return funcs, sinks
