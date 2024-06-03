import os
import pandas as pd

def calculate_compression_ratio(original_size, compressed_size):
    return original_size / compressed_size if compressed_size != 0 else 0

def get_file_size(file_path):
    return os.path.getsize(file_path)

def main():
    # Укажите пути к оригинальным и сжатым файлам
    files = {
        'test.bmp': 'test.bmp.zip',
        'R_r1.bmp': 'R_r1.bmp.zip',
        'M_r1.bmp': 'M_r1.bmp.zip',
        'H.bmp': 'H.bmp.zip',
        'R_r2.bmp': 'R_r2.bmp.zip',
        'M_r2.bmp': 'M_r2.bmp.zip',
        'H.bmp': 'H.bmp.zip',
        'R_r3.bmp': 'R_r3.bmp.zip',
        'M_r3.bmp': 'M_r3.bmp.zip',
        'H.bmp': 'H.bmp.zip',
        # добавьте столько файлов, сколько нужно
    }

    data = []

    for original, compressed in files.items():
        original_size = get_file_size(original)
        compressed_size = get_file_size(compressed)
        compression_ratio = calculate_compression_ratio(original_size, compressed_size)

        data.append({
            'Original File': original,
            'Compressed File': compressed,
            'Compressed Size (bytes)': compressed_size,
            'Compression Ratio': compression_ratio
        })

    df = pd.DataFrame(data)
    print(df)

    # Сохранить таблицу в файл, если нужно
    df.to_csv('compression_ratios.csv', index=False)

if __name__ == "__main__":
    main()
