from app.image_processing.image_processing import ImageProcessor


def create_database():
    processor = ImageProcessor()
    processor.load_images("../../data")
    processor.decrease_resolutions(3)  # 168x168 * (1/3) = 56x56
    processor.rotate_images(60)
    processor.zoom_all()
    processor.reduce_colors(color_amount=2)
    processor.replace_darkest_color(new_color=(0, 0, 0))  # zamienia tlo na czarne
    processor.change_color()
    processor.mirror()
    processor.save()


if __name__ == '__main__':
    create_database()