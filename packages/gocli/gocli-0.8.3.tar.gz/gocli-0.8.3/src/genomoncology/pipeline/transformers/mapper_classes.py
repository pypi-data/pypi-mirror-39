from genomoncology.parse.doctypes import DocType, __TYPE__, __CHILD__
from .registry import register, get_transformer


class VariantMapper(object):
    """
    Variant is a Call with additional meta information such as file_path,
    build, pipeline, run_id.

    Also, all of the 'info' fields are inserted to to the top-level of the
    document with wild-card typing format (e.g. DP__mint, etc.)
    """

    def __init__(self, **meta):
        self.meta = {k: v for (k, v) in meta.items() if v is not None}
        self.types = {}

    def resolve_info_key(self, k):
        return f"{k}__{self.types.get(k, 'string')}"

    def __call__(self, doc):
        if DocType.HEADER.is_a(doc):
            self.types = doc.get("types", {})
            self.meta["file_path"] = doc.get("file_path", None)

            # todo: replace copy with cytoolz
            header = doc.copy()
            header[__CHILD__] = doc.get(__CHILD__, "").replace(
                "CALL", "VARIANT"
            )
            return header

        elif DocType.VARIANT.is_a(doc):
            return doc

        elif DocType.TSV.is_a(doc) or DocType.ANNOTATED_TSV.is_a(doc):
            variant = doc.copy()
            variant.pop("annotations", None)
            variant[__TYPE__] = "VARIANT"
            variant.update(self.meta)
            return variant

        elif DocType.CALL.is_a(doc) or DocType.ANNOTATED_CALL.is_a(doc):
            # todo: replace copy with cytoolz
            # todo: replace with registered function, remove this elif
            variant = doc.copy()
            variant.pop("annotations", None)
            variant[__TYPE__] = doc.get(__TYPE__).replace("CALL", "VARIANT")
            variant.update(self.meta)
            info = variant.pop("info", {})
            info = {self.resolve_info_key(k): v for (k, v) in info.items()}
            variant.update(info)
            return variant

        else:
            tx = get_transformer(DocType.VARIANT, doc.get(__TYPE__))
            return tx(doc)


register(transformer=VariantMapper, output_type=DocType.VARIANT)
