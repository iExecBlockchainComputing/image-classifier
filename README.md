# tf-image-classifier
Trusted execution tensorflow application that protects the prediction model of a classification program.   

## input

  
- The mobilenetv1.h5 keras model
- The image classes index file
```json
{"0": ["n01440764", "tench"], 
"1": ["n01443537", "goldfish"], 
"2": ["n01484850", "great_white_shark"],
"3": ["n01491361", "tiger_shark"], 
"4": ["n01494475", "hammerhead"]
...}
```

- The images to be classified 

![bridge.jpg](https://github.com/iExecBlockchainComputing/image-classifier/blob/main/local_run/bridge.jpg?raw=true)
![mountain.jpg](https://github.com/iExecBlockchainComputing/image-classifier/blob/main/local_run/mountain.jpg?raw=true)

*Use 224 x 224 images for better results, examples can be found here https://picsum.photos/224
otherwise, the images will be resized automatically. The program reads only files ending in .jpg or .JPG*

## output

  

the classified files and their scores :

```json
{
	"0": {
		"filename": "bridge.jpg",
		"predictions": {
			"0": {
				"class": "n04366367",
				"description": "suspension_bridge",
				"score": 0.9888280630111694
			},
			"1": {
				"class": "n03933933",
				"description": "pier",
				"score": 0.0090409554541111
			},
			"2": {
				"class": "n03947888",
				"description": "pirate",
				"score": 0.0017763386713340878
			},
			"3": {
				"class": "n04147183",
				"description": "schooner",
				"score": 0.0001802647893782705
			},
			"4": {
				"class": "n04311004",
				"description": "steel_arch_bridge",
				"score": 0.0001498213387094438
			}
		}
	},
	"1": {
		"filename": "mountain.jpg",
		"predictions": {
			"0": {
				"class": "n09193705",
				"description": "alp",
				"score": 0.16904009878635406
			},
			"1": {
				"class": "n04008634",
				"description": "projectile",
				"score": 0.13410575687885284
			},
			"2": {
				"class": "n02951358",
				"description": "canoe",
				"score": 0.09152363240718842
			},
			"3": {
				"class": "n09332890",
				"description": "lakeside",
				"score": 0.0898909792304039
			},
			"4": {
				"class": "n09468604",
				"description": "valley",
				"score": 0.08329412341117859
			}
		}
	}
}
```



 

### Running locally

    docker run --rm -v ${PWD}/local_run:/iexec_out -e IEXEC_OUT=/iexec_out \
    -v ${PWD}/local_run:/iexec_in -e IEXEC_IN=/iexec_in \
    -e IEXEC_DATASET_FILENAME=mobilenetv1.h5 -e IEXEC_REQUESTER_SECRET_1="Rw[/2GY@" tf-image-classifier:latest

  
### Running in iExec

  
Considering the image has been sconified,secret deployed, app deployed and dataset encrypted and deployed


iexec app run 0xE86481eCF9CB8cb9c2f08D2067f8265a709fDdFB \
    --tag tee --dataset 0xa9ed83C91D8311A2B52A6f5efd5A3196D635f53D \
    --workerpool v7-debug.main.pools.iexec.eth \
    --secret 1=zip_pwd \
    --params {\"iexec_developer_logger\":true} \
    --chain bellecour --input-files \
    https://raw.githubusercontent.com/iExecBlockchainComputing/image-classifier/multisecret/local_run/input_images.zip,https://raw.githubusercontent.com/iExecBlockchainComputing/image-classifier/multisecret/local_run/imagenet_class_index.json

