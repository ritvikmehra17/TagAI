from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

def execute(image_path):
    authenticator=IAMAuthenticator('fZSpq0XcLXx3SaEbJTsAux2f0sGtrUxl6pemvYYauSvx')
    visual_recognition=VisualRecognitionV3(version='2018-03-19',authenticator=authenticator)
    visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/5358c9dd-186b-4149-a8f0-ae4c9a30beb2')
    print(image_path)

    with open(image_path,'rb') as images_file:
        classes=visual_recognition.classify(images_file=images_file).get_result()
        json_data=json.loads(json.dumps(classes,indent=2))
        type(json_data)
        #print(json_data)
        return (json_data)

if __name__ == "__main__":
    output=execute('uploads/img_20191227163725.jpg')
