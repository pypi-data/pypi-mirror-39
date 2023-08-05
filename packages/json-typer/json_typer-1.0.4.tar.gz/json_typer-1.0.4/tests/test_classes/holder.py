from json_typer import TypeSerializable


class Holder(TypeSerializable):
    def __init__(self, *args, **kwargs):
        super(Holder, self).__init__(*args, **kwargs)

        self.objects = []
