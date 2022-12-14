from Helpers import Requests
from Helpers import DB
from PIL import Image
import os
import hashlib
from datetime import datetime


class Files:
    def __init__(self, *args):
        if not os.path.exists('public'):
            os.mkdir('public')
        if not os.path.exists('public/products'):
            os.mkdir('public/products')
        if not os.path.exists('public/products/photos'):
            os.mkdir('public/products/photos')

        self.logging = args[0]
        self.request = Requests.Requests('files', None, *args)
        self.db = DB.Connection(*args)

    def upload_image(self, images, id):
        for i, image in enumerate(images):

            img = Image.open(self.request.get(image['href'], stream=True).raw)
            name = hashlib.md5((str(id) + 'img-' + str(i + 1)).encode()).hexdigest()
            is_image = self.db.fetch_one('SELECT * FROM media WHERE name=%s', (name,))
            if is_image:
                continue
            ext = '.png'
            mimeType = 'image/png'
            if img.format == 'JPEG':
                ext = '.jpg'
                mimeType = 'image/jpeg'
            if not os.path.exists('public/products/photos/' + str(id)):
                os.mkdir('public/products/photos/' + str(id))

            save_dir = 'public/products/photos/' + str(id) + '/'

            # Save to dir
            file_name = name + ext
            img.save(save_dir + file_name)

            # Save to db
            sql = "INSERT INTO media (model_type,model_id,collection_name,name,file_name,mime_type,disk,conversions_disk,size,manipulations,custom_properties,generated_conversions,responsive_images,order_column,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            inserted = self.db.insert_return_id(sql, ('Modules\Ecommerce\Entities\Products', id, 'product_photos', name, file_name, mimeType, 'products', 'products', os.stat(save_dir + file_name).st_size, '[]', '[]', '{"product_photos_resized": true}', '[]', i, datetime.now(), datetime.now(),))
            if inserted:
                os.rename(save_dir, 'public/products/photos/' + str(inserted))
        return True
