from deep_translator import GoogleTranslator
import time

def Google_Trans(input_text):
    try:
        translated = GoogleTranslator(source='zh-CN', target='en').translate(input_text)
        return translated
    except Exception as e:
        print("Translator Module error"+str(e))
        print("\nCooling off for 30 secs")
        time.sleep(30)
        translated = Google_Trans(input_text)
        return translated

def main():
	while(True):
		text = "西黑冠长臂猿种群数量呈稳中有升趋势"
		result = Google_Trans(text)
		print(result)
		print("Sleeping")
		time.sleep(10)

if __name__ == "__main__":
    main()
   
