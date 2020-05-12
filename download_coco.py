from pycocotools.coco import COCO
import requests
import os

cat_of_interest = "person" # supports only one category.

coco = COCO('./instances_train2017.json')
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
# print('COCO categories: \n{}\n'.format(' '.join(nms)))

catIds = coco.getCatIds(catNms=[cat_of_interest])
# imgIds = coco.getImgIds(catIds=catIds )
# images = coco.loadImgs(imgIds)
# print("imgIds: ", imgIds)
# print("images: ", images)

ann_ids = coco.getAnnIds(catIds=catIds, iscrowd=None)
all_ann = coco.loadAnns(ann_ids)
 
df_rows = []
for i in range(0, len(all_ann)):
    cur_ann = all_ann[i]
    cbbox = cur_ann["bbox"]
    images = coco.loadImgs(cur_ann["image_id"])

    if(len(images) > 1):
        print("ERROR: More than one image got loaded")
        sys.exit(1)

    print("im: ", images[0], cbbox)
    if(not os.path.exists('./downloaded_images/' + images[0]['file_name'])):
        img_data = requests.get(images[0]['coco_url']).content
        with open('./downloaded_images/' + images[0]['file_name'], 'wb') as handler:
            handler.write(img_data)
        
        filename   = images[0]["file_name"]
        cur_class  = cat_of_interest
        width    = images[0]["width"]
        height   = images[0]["height"]
        xmin     = int(cbbox[0])
        ymin     = int(cbbox[1])
        xmax     = min(int(xmin + cbbox[2]), width-1)
        ymax     = min(int(ymin + cbbox[3]), height-1)

        with open('./downloaded_labels/' + images[0]['file_name'][:-4] + '.txt', 'w') as f:
            f.write(str([filename, cur_class, width, height, ymin, xmin, ymax, xmax]))

# for im in images:
#     print("im: ", im)
#     img_data = requests.get(im['coco_url']).content
#     with open('downloaded_images/' + im['file_name'], 'wb') as handler:
#         handler.write(img_data)