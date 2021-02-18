from io import BytesIO

class PRMP_File(BytesIO):

    def __init__(self, filename='', base64=b'', data=b''):

        passed = [bool(a) for a in [filename, base64]].count(True)
        assert passed <= 1, 'Only one is required in [filename, base64, image]'

        self.name = None
        self._data = data

        if data: self.name = 'data_%d'%PRMP_ImageFile.count

        elif filename:
            self.name = os.path.basename(filename)
            if inbuilt: self._data = PRMP_Images.get(filename, inExt)
            else: self._data = open(filename, 'rb').read()

        elif base64:
            self._data = b64decode(base64)
            self.name = 'base64_%d'%PRMP_ImageFile.count

        super().__init__(self._data)

        if image: image.save(self, inExt)

        PRMP_ImageFile.count += 1