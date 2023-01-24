from pathlib import Path

import easyocr
import pandas as pd


class Extractor:

    ALLOW_SUFFIXES = ['.jpg', '.jpeg', '.png']

    def __init__(self, folder_path, post_process: callable = None):
        self.image_folder_path = Path(folder_path)
        self.reader = easyocr.Reader(['ch_sim', 'en'])
        self.post_process = post_process

    def _is_image(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.ALLOW_SUFFIXES

    def extract(self, output_file: str = 'list.csv', default_score: int = 8):
        files = self.image_folder_path.glob('*')
        filtered_files = []

        for file in files:
            if self._is_image(file):
                filtered_files.append(file)

        extracted_text = []
        img_source = []

        for img_path in filtered_files:
            print(f'Extracting text on {img_path}')
            results = self.reader.readtext(str(img_path))

            for result in results:
                if self.post_process:
                    result = self.post_process(result)

                if result[1]:
                    img_source.append(str(img_path))
                    extracted_text.append(result[1])
            print(f'Finished OCR for {img_path}')

        scores = [default_score] * len(extracted_text)
        data = dict(name=extracted_text, source=img_source, score=scores)
        df = pd.DataFrame(data=data)
        df.to_excel('list.xlsx', index=False)


if __name__ == '__main__':

    def post_process(result):
        coordinates = result[0]
        max_y = 0
        min_y = float('inf')
        min_x = float('inf')

        for coordinate in coordinates:
            if coordinate[1] > max_y:
                max_y = coordinate[1]

            if coordinate[1] < min_y:
                min_y = coordinate[1]
            
            if coordinate[0] < min_x:
                min_x = coordinate[0]

        text = result[1]

        KEYWORDS = ['我的评分', '分钟', '上映日期', '动作', '观影时间']

        for keyword in KEYWORDS:
            if keyword in text:
                return (None, None, None)
        
        if max_y - min_y < 60 or min_x < 280 or min_x > 295:
            result = (None, None, None)
        return result

    extractor = Extractor('samples', post_process=post_process)
    extractor.extract()
