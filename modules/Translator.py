from deep_translator import GoogleTranslator
import time
import translators as ts
import random

def Google_Trans(input_text):
    try:
        translated = GoogleTranslator(source='zh-CN', target='en').translate(input_text[0:5000])
        return translated
    except Exception as e:
        print("Translator Module error"+str(e))
        print("\nCooling off for 10 secs")
        time.sleep(10)
        translated = random_translator(input_text[0:5000])
        return translated


def random_translator(q_text):
    translators = ['alibaba','bing','cloudTranslation','google','iciba','iflyrec','itranslate','lingvanex','modernMt','papago','qqFanyi','qqTranSmart','reverso','sogou','translateCom','youdao']
    selected_translator = random.choice(translators)
    #print(selected_translator)
    try:
        translated = ts.translate_text(q_text[0:5000],translator=selected_translator,from_language='zh',to_language='en')
        return translated
    except Exception as e:
        print("Translator Module error"+str(e))
        print("\nCooling off for 10 secs")
        time.sleep(10)
        translated = Google_Trans(q_text[0:5000])
        return translated




def main():
	while(True):
		text = "九三軍人節即將到來，文化總會1日發布最新一集《匠人魂》，介紹國防部軍備局生產製造中心第205廠（205廠）士官長柯俊文，以其設計的槍械和刺刀，展現國軍追求卓越的堅持。文總秘書長李厚慶表示，文總自2018年起，每年軍人節皆推出一集以國軍為主角的《匠人魂》，包含製降落傘、修復軍艦、戰車修護、戰鬥機檢修、直升機保修，不僅是祝賀軍人節快樂，更希望透過國軍的職人身影，讓大眾更深入了解國軍。文總說明，本次《匠人魂》的主角柯俊文，高職就讀機械相關科系，一畢業便報考士官班，輾轉進入專責研發與生產輕兵器的205廠。即使軍事科技日新月異，機動性高的槍械仍是國防重要配備，輕量化、適用國造彈藥、適合亞洲人體型的T75班用機槍，參考自比利時FN Minimi輕機槍，為205廠於1986年研製的國造兵器。T75班用機槍因應作戰實需不斷進化，柯俊文也參與了近期的結構改良專案。柯俊文研究每一種型式的輕兵器，熟悉每一個零組件，每項設計專案皆經過嚴謹的評估與資料蒐整，在進行3D繪圖的過程中，零件便一一在柯俊文腦內同步模擬媒合，他根據設計原理，思索組裝道次，依序組合出由小到大的總成，逐漸疊加為一支全槍。柯俊文說：「一枝槍的設計，過程中一定會遇到很多問題，因此需要好幾次反覆地去驗證它。」每一處變更都將影響整體結構，除了需要恆久的耐心，也仰賴專業團隊的合作。柯俊文位居協調角色，除了和加工所師傅討論零件製作的可行性，也必須與設計同仁再三驗證或修改設計，串連整個工作團隊，共同克服大大小小的技術問題。除了槍械，脫胎自美軍M9刺刀的多功能戰鬥匕首，兼具戰鬥力與實用性，不僅可變形成破壞剪，並可充作一字起子等工具。生於排灣族家庭的柯俊文，對刀具最深刻的印象，是家中父兄無論上山下田，從不離身的那把山刀。他設計完這把多功能刺刀時，想起了排灣族的代表性百步蛇圖騰，經柯俊文之手，多功能戰鬥匕首有百步蛇低調匍匐，刀鞘的菱格紋一路蜿蜒，至手柄撫觸如蛇腹，呈現兼具機能與美感的設計，也因此有了本集《匠人魂》的命名「百步穿楊」。"
		result = random_translator(text)
		print(result, file=open('output.txt', 'a'))
		print("Sleeping")
		time.sleep(10)

if __name__ == "__main__":
    main()
   
