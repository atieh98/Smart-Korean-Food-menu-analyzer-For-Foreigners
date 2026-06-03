# ======================================================================================
# 🧠 ALGORITHMIC ENGINE    | GLOBAL TEXT-BLOCK PARSER & RESILIENT SUBSTRING MATCH
# 📄 FILE NAME             | menu_analyzer.py
# --------------------------------------------------------------------------------------
# 🔍 ENGINE CONFIGURATION  | PyTesseract OCR with Global Pattern Matching
# ⚡ TOLERANT FUZZY LOGIC  | [1] Global Block Inclusions [2] Spaced Regex [3] Near-Neighbor
# ======================================================================================

import os
import pytesseract
import re

class SmartMenuAnalyzer:
    def __init__(self, tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        # 🛡️ Cross-Platform Tesseract Path Handler
        if os.name == 'nt':  # Check if the environment is Windows
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        # On Linux/Streamlit Cloud, it skips this block and automatically finds 'tesseract' in system PATH
        
        # Full menu-specific database synced with your target restaurant
        self.food_database = {
            # --- GIMBAP VARIETIES (김밥류) ---
            "원조김밥": {"english_name": "Original Gimbap", "description": "Classic rice roll wrapped in seaweed with yellow radish, egg, ham, and burdock root.", "spicy_level": "❌ Non-spicy", "pork_included": "Maybe (Contains Ham)", "allergies": "Egg, Wheat, Pork"},
            "야채김밥": {"english_name": "Vegetable Gimbap", "description": "Rice roll packed with extra fresh vegetables like carrots, spinach, and cucumbers.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Egg, Sesame"},
            "김치김밥": {"english_name": "Kimchi Gimbap", "description": "Savory seaweed rice roll stuffed with well-fermented stir-fried Kimchi.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Egg, Sesame, Soybean"},
            "치즈김밥": {"english_name": "Cheese Gimbap", "description": "Gimbap with a rich, savory slice of processed American cheddar cheese inside.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Milk, Egg, Wheat"},
            "참치김밥": {"english_name": "Tuna Gimbap", "description": "Highly popular gimbap filled with savory canned tuna mixed with creamy mayonnaise.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Fish, Egg, Milk"},
            "계란말이김밥": {"english_name": "Egg Roll Gimbap", "description": "A classic roll wrapped inside or filled with a thick, comforting layer of rolled omelet.", "spicy_level": "❌ Non-spicy", "pork_included": "Maybe (Ham)", "allergies": "Egg, Wheat"},
            "멸치김밥": {"english_name": "Anchovy Gimbap", "description": "Seaweed rice roll filled with savory, sweet, and crispy seasoned dried baby anchovies.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Fish, Sesame, Soybean"},
            "소고기김밥": {"english_name": "Beef Gimbap", "description": "Seaweed rice roll packed with savory minced soy-marinated beef and fresh vegetables.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Beef, Soybean, Wheat, Egg"},
            "돈까스김밥": {"english_name": "Pork Cutlet Gimbap", "description": "Seaweed rice roll stuffed with a crispy piece of deep-fried breaded pork cutlet.", "spicy_level": "❌ Non-spicy", "pork_included": "⚠️ YES", "allergies": "Pork, Wheat, Egg, Milk"},
            "고추참치김밥": {"english_name": "Spicy Chili Tuna Gimbap", "description": "Seaweed rice roll featuring canned tuna mixed with a fiery, sweet hot pepper sauce.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Fish, Egg, Soybean"},
            "새우김밥": {"english_name": "Fried Shrimp Gimbap", "description": "Seaweed rice roll containing a whole crispy golden deep-fried breaded shrimp.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Shrimp/Crustacean, Wheat, Egg"},
            "모듬김밥": {"english_name": "Assorted Combo Gimbap", "description": "Large mega-gimbap combining tuna, cheese, and vegetable fillings altogether.", "spicy_level": "❌ Non-spicy", "pork_included": "Maybe (Ham)", "allergies": "Egg, Milk, Fish, Pork"},
            "진미채김밥": {"english_name": "Spicy Squid Strips Gimbap", "description": "Seaweed rice roll filled with chewy, sweet, and spicy seasoned dried squid shreds.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Squid, Sesame, Soybean"},
            "제육김밥": {"english_name": "Spicy Pork Gimbap", "description": "Seaweed rice roll stuffed with savory, smoky stir-fried spicy marinated pork.", "spicy_level": "🌶️ (Mild)", "pork_included": "⚠️ YES", "allergies": "Pork, Soybean, Sesame, Egg"},
            "땡초김밥": {"english_name": "Spicy Chili Gimbap", "description": "Fiery rice roll loaded with finely chopped hot green cheongyang chili peppers.", "spicy_level": "🌶️🌶️🌶️ (Hot)", "pork_included": "❌ NO", "allergies": "Egg, Sesame"},
            "삼겹살김밥": {"english_name": "Pork Belly Gimbap", "description": "Premium seaweed rice roll packed with grilled pork belly, savory ssamjang sauce, and green peppers.", "spicy_level": "🌶️ (Mild)", "pork_included": "⚠️ YES", "allergies": "Pork, Soybean, Wheat, Egg"},
            "샐러드김밥": {"english_name": "Salad Gimbap", "description": "Light, crunchy gimbap stuffed with fresh cabbage/crab salad and sweet mayonnaise.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Egg, Milk, Crab/Crustacean"},
            "누드김밥": {"english_name": "Nude Gimbap", "description": "Inverted sushi-style gimbap where the seasoned rice layer is on the outside.", "spicy_level": "❌ Non-spicy", "pork_included": "Maybe (Ham)", "allergies": "Egg, Wheat, Sesame"},
            "멸추김밥": {"english_name": "Anchovy & Chili Gimbap", "description": "Gimbap filled with stir-fried spicy dried baby anchovies and green chilies.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Fish, Soybean"},

            # --- CUTLET VARIETIES (돈까스류) ---
            "등심돈까스": {"english_name": "Pork Loin Cutlet", "description": "Crispy deep-fried breaded pork cutlet made from premium, tender loin meat.", "spicy_level": "❌ Non-spicy", "pork_included": "⚠️ YES", "allergies": "Pork, Wheat, Milk, Egg"},
            "치즈돈까스": {"english_name": "Cheese Pork Cutlet", "description": "Crispy breaded pork cutlet core filled heavily with premium melted mozzarella cheese.", "spicy_level": "❌ Non-spicy", "pork_included": "⚠️ YES", "allergies": "Wheat, Pork, Milk"},
            "고구마치즈돈까스": {"english_name": "Sweet Potato Cheese Pork Cutlet", "description": "Crispy breaded pork cutlet stuffed with sweet potato puree and gooey mozzarella cheese.", "spicy_level": "❌ Non-spicy", "pork_included": "⚠️ YES", "allergies": "Pork, Wheat, Milk, Egg"},
            "돈까스": {"english_name": "Pork Cutlet", "description": "Giant, crispy deep-fried breaded pork cutlet served with sweet savory brown gravy.", "spicy_level": "❌ Non-spicy", "pork_included": "⚠️ YES", "allergies": "Wheat, Pork, Milk"},
            "스페셜정식": {"english_name": "Special Combo Set", "description": "The ultimate combination platter combining pork cutlet, gimbap, and jjolmyeon noodles.", "spicy_level": "🌶️ (Mild)", "pork_included": "⚠️ YES", "allergies": "Pork, Wheat, Milk, Egg"},

            # --- STEWS & SOUPS (찌개류) ---
            "김치찌개": {"english_name": "Kimchi Jjigae", "description": "Deeply savory, hot stew cooked with aged kimchi, tofu, and fatty pork pieces.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "⚠️ YES (Contains Pork)", "allergies": "Soybean, Pork"},
            "참치찌개": {"english_name": "Chamchi Jjigae", "description": "Spicy stew cooked with oil-marinated canned tuna fish, tofu, and onions.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Soybean, Fish"},
            "된장찌개": {"english_name": "Doenjang Jjigae", "description": "Traditional earthy stew made with fermented soybean paste, tofu, and zucchini.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Soybean"},
            "순두부찌개": {"english_name": "Sundubu Jjigae", "description": "Spicy, silky stew featuring ultra-soft tofu curd simmered with vegetables and an egg.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "Maybe", "allergies": "Soybean, Egg"},
            "부대찌개": {"english_name": "Budae Jjigae", "description": "Spicy fusion stew packed with ham, sausages, spam, baked beans, and ramen noodles.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "⚠️ YES (Pork processing meats)", "allergies": "Wheat, Soy, Pork"},
            "짬뽕밥": {"english_name": "Spicy Seafood Soup with Rice", "description": "Fiery, smoky seafood soup loaded with vegetables, pork bits, served with a bowl of rice.", "spicy_level": "🌶️🌶️🌶️ (Hot)", "pork_included": "⚠️ YES (Contains pork broth bits)", "allergies": "Seafood, Pork, Soybean, Wheat"},
            "육개장": {"english_name": "Yukgaejang", "description": "Fiery shredded beef soup slow-simmered with scallions, fernbrake, and glass noodles.", "spicy_level": "🌶️🌶️🌶️ (Hot)", "pork_included": "❌ NO", "allergies": "Sesame, Soybean, Beef"},
            "갈비탕": {"english_name": "Galbitang", "description": "Clear, premium, nourishing soup made by boiling large beef short ribs and radish.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Wheat, Beef"},
            "오뎅": {"english_name": "Odeng (Fish Cake Soup)", "description": "Skewered fish cakes simmered in a light radish-anchovy stock stock.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Fishcake, Wheat"},
            "오뎅매운탕(공기밥)": {"english_name": "Spicy Fish Cake Stew (with Rice)", "description": "A hot, fiery, and extra spicy fish cake hotpot soup served alongside a bowl of rice.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Fishcake, Wheat, Soybean"},
            "황태해장국": {"english_name": "Dried Pollack Hangover Soup", "description": "A deeply soothing, clear hangover soup simmered with dried pollack, white radish, and egg flakes.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Fish, Egg, Soybean"},
            "뚝배기불고기": {"english_name": "Ttukbaegi Bulgogi", "description": "Sweet soy-marinated beef ribbons simmered with onions and glass noodles in a clay pot.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Soybean, Wheat, Beef"},
            "해물순두부찌개": {"english_name": "Haemul Sundubu Jjigae", "description": "Spicy soft tofu stew enriched with shrimp, squid, clams, and mussels.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Soybean, Seafood, Shellfish"},
            "참치김치찌개": {"english_name": "Chamchi Kimchi Jjigae", "description": "Spicy kimchi stew cooked with rich canned tuna instead of traditional pork bits.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Soybean, Fish"},
            "고등어찌개": {"english_name": "Mackerel Stew", "description": "Spicy, rich mackerel fish stew simmered with thick layers of savory white radish.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Fish, Soybean"},
            "콩나물국밥": {"english_name": "Kongnamul Gukbap", "description": "Cleansing, hot sprout soup served with rice submerged inside the broth.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Sesame, Egg"},

            # --- TTEOKBOKKI VARIETIES (떡볶이류) ---
            "떡볶이": {"english_name": "Tteokbokki", "description": "Chewy rice cakes and fish cakes simmered in a thick, sweet red pepper sauce.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Fishcake"},
            "라볶이": {"english_name": "Rabokki", "description": "A delicious combination of instant ramen noodles and rice cakes cooked in tteokbokki sauce.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Fishcake"},
            "쫄볶이": {"english_name": "Jjolbokki", "description": "Super chewy jjolmyeon wheat noodles cooked inside hot and sweet spicy tteokbokki sauce.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Fishcake"},
            "치즈떡볶이": {"english_name": "Cheese Tteokbokki", "description": "Chewy rice cakes cooked in sweet red pepper sauce topped with abundant melted mozzarella.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Milk, Wheat, Fishcake"},
            "치즈라볶이": {"english_name": "Cheese Rabokki", "description": "Sweet and spicy rabokki smothered under an abundant blanket of melted mozzarella.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Wheat, Fishcake, Milk"},
            "군만두(6개)": {"english_name": "Fried Dumplings (6pcs)", "description": "Six pieces of crispy golden-fried Korean dumplings filled with seasoned pork and chives.", "spicy_level": "❌ Non-spicy", "pork_included": "⚠️ YES", "allergies": "Wheat, Pork, Soybean"},

            # --- NOODLE VARIETIES (면류) ---
            "라면": {"english_name": "Ramen", "description": "Instant curly noodles in a hot, savory and spicy beef or vegetable broth.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Soybean"},
            "떡라면": {"english_name": "Rice Cake Ramen", "description": "Spicy instant ramen boiled with soft, sliced cylindrical Korean rice cakes.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Soybean"},
            "치즈라면": {"english_name": "Cheese Ramen", "description": "Hot instant ramen topped with a slice of melted cheese to create a creamy broth.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Wheat, Milk, Soybean"},
            "만두라면": {"english_name": "Dumpling Ramen", "description": "Spicy instant ramen served with several plump Korean dumplings inside.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "⚠️ YES (Dumplings contain pork)", "allergies": "Wheat, Pork, Soybean"},
            "콩나물라면": {"english_name": "Bean Sprout Ramen", "description": "Spicy instant ramen boiled with crunchy fresh soybean sprouts for a crisp, refreshing stock.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Soybean"},
            "김치라면": {"english_name": "Kimchi Ramen", "description": "Instant ramen simmered with tangy fermented kimchi for a sour, fiery kick.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Soybean"},
            "통계란라면": {"english_name": "Whole Egg Ramen", "description": "Spicy instant ramen upgraded with a whole cooked egg poached directly in the hot savory broth.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Egg, Soybean"},
            "짬뽕라면": {"english_name": "Jjambong Seafood Ramen", "description": "Extra fiery, smoky instant ramen mimicking Chinese-Korean seafood noodle soup.", "spicy_level": "🌶️🌶️🌶️ (Hot)", "pork_included": "Maybe", "allergies": "Wheat, Seafood, Shellfish"},
            "부대라면": {"english_name": "Budae Ramen", "description": "Spicy instant ramen loaded with sliced sausages, spam, and processed ham in an army-stew layout.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "⚠️ YES", "allergies": "Wheat, Pork, Soybean"},
            "우동": {"english_name": "Udon Noodle Soup", "description": "Thick, chewy wheat noodles immersed in a hot, mild, soothing soy-anchovy broth.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Wheat, Fishcake"},
            "김치우동": {"english_name": "Kimchi Udon Noodles", "description": "Thick, chewy udon wheat noodles cooked in a hot, tangy, and savory fermented kimchi soup.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Wheat, Soybean, Fishcake"},
            "멸치국수": {"english_name": "Anchovy Noodle Soup", "description": "Thin flour noodles served hot in a clean, comforting, and remarkably light anchovy stock broth.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Wheat, Fish"},
            "비빔국수": {"english_name": "Spicy Mixed Noodles", "description": "Thin wheat noodles tossed thoroughly in a sweet, savory, and sharp spicy chili paste.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Sesame"},
            "칼국수": {"english_name": "Knife-Cut Noodles", "description": "Thick, flat handmade wheat noodles served hot in a deep, rich savory broth.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Wheat, Soybean"},
            "김치칼국수": {"english_name": "Kimchi Kalguksu", "description": "Flat, knife-cut wheat noodles served steaming hot in a spicy, comforting kimchi soup.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Soybean"},
            "얼큰이해물국수": {"english_name": "Fiery Seafood Noodle Soup", "description": "Wheat noodles served in an extra hot, fiery broth packed heavily with mixed seafood pieces.", "spicy_level": "🌶️🌶️🌶️ (Hot)", "pork_included": "❌ NO", "allergies": "Wheat, Seafood, Shellfish"},
            "쫄면": {"english_name": "Jjolmyeon", "description": "Highly rubbery cold wheat noodles tossed in a sharp sweet, sour, and fiery chili paste.", "spicy_level": "🌶️🌶️ (Medium)", "pork_included": "❌ NO", "allergies": "Wheat, Sesame"},
            "냉면(계절음식)": {"english_name": "Chilled Buckwheat Cold Noodles (Seasonal)", "description": "Refreshing summer cold buckwheat noodles submersed inside an icy, tangy broth slurry.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Buckwheat, Wheat, Beef"},
            "떡국": {"english_name": "Rice Cake Soup", "description": "Sliced oval rice cakes cooked in a savory, mild beef or egg broth, topped with seaweed.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Wheat, Egg, Beef"},
            "만두국": {"english_name": "Dumpling Soup", "description": "Plump savory dumplings simmered in a warm, comforting egg and rib broth.", "spicy_level": "❌ Non-spicy", "pork_included": "⚠️ YES", "allergies": "Wheat, Pork, Egg"},
            "떡만두국": {"english_name": "Rice Cake & Dumpling Soup", "description": "Rice cake soup combined beautifully with hearty Korean pork dumplings.", "spicy_level": "❌ Non-spicy", "pork_included": "⚠️ YES", "allergies": "Wheat, Pork, Egg"},

            # --- MEALS & RICE BOWLS (덮밥류) ---
            "제육덮밥": {"english_name": "Spicy Pork Rice Bowl", "description": "Thin sliced pork shoulder stir-fried in a sweet, smoky chili glaze over rice.", "spicy_level": "🌶️🌶️🌶️ (Hot)", "pork_included": "⚠️ YES", "allergies": "Pork, Soybean, Sesame"},
            "오징어덮밥": {"english_name": "Squid Rice Bowl", "description": "Squid sliced into rings and flash-fried in a fiery gochujang sauce over rice.", "spicy_level": "🌶️🌶️🌶️ (Hot)", "pork_included": "❌ NO", "allergies": "Squid, Soybean"},
            "참치덮밥": {"english_name": "Tuna Rice Bowl", "description": "Rice bowl topped with stir-fried tuna, fresh vegetables, and savory seaweed flakes.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Fish, Sesame"},
            "불고기덮밥": {"english_name": "Bulgogi Rice Bowl", "description": "Sweet soy-marinated thinly sliced beef stir-fried with vegetables and served over warm rice.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Beef, Soybean, Wheat, Sesame"},
            "치킨마요덮밥": {"english_name": "Chicken Mayo Rice Bowl", "description": "Rice topped with savory fried chicken strips, scrambled egg shreds, mayonnaise, and soy glaze.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Chicken, Egg, Soybean, Wheat, Milk"},
            "알밥": {"english_name": "Fish Roe Rice Bowl", "description": "Sizzling hot stone pot rice topped with colorful, popping fish roe and radish pickles.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Fish Roe, Sesame"},
            "김치알밥": {"english_name": "Kimchi Fish Roe Rice Bowl", "description": "Sizzling hot stone pot rice topped with popping fish roe, pickled radish, and finely chopped sautéed kimchi.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Fish Roe, Sesame, Soybean"},
            "비빔밥": {"english_name": "Bibimbap", "description": "Warm rice topped with assorted seasoned vegetables, chili paste, and a fried egg.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Egg, Sesame, Soy"},
            "돌솥비빔밥": {"english_name": "Dolsot Bibimbap", "description": "Bibimbap served inside a sizzling hot stone pot to create a crunchy rice bottom.", "spicy_level": "🌶️ (Mild)", "pork_included": "❌ NO", "allergies": "Egg, Sesame, Soy"},
            "낙지돌솥밥": {"english_name": "Spicy Octopus Stone Pot Rice", "description": "Sizzling stone pot rice topped with tender, ultra-spicy stir-fried octopus and green vegetables.", "spicy_level": "🌶️🌶️🌶️ (Hot)", "pork_included": "❌ NO", "allergies": "Octopus, Seafood, Soybean, Sesame"},
            "불백비빔밥": {"english_name": "Bulgogi Pork Rice Mix", "description": "A unique style of bibimbap featuring savory charcoal-flavored stir-fried pork bulgogi as the main topping.", "spicy_level": "🌶️ (Mild)", "pork_included": "⚠️ YES", "allergies": "Pork, Soybean, Sesame, Egg"},
            "오므라이스": {"english_name": "Omurice", "description": "Fried rice wrapped inside a fluffy, smooth omelet sheet, drizzled with sweet gravy.", "spicy_level": "❌ Non-spicy", "pork_included": "Maybe", "allergies": "Egg, Wheat, Milk"},
            "카레라이스": {"english_name": "Curry Rice Platter", "description": "A generous serving of smooth, comforting traditional yellow Korean curry with potatoes and onions over rice.", "spicy_level": "❌ Non-spicy", "pork_included": "Maybe", "allergies": "Wheat"},
            "김치볶음밥": {"english_name": "Kimchi Fried Rice", "description": "Rice wok-fried with chopped sour kimchi, topped with a gorgeous runny fried egg.", "spicy_level": "🌶️ (Mild)", "pork_included": "Maybe", "allergies": "Egg, Soybean, Pork"},
            "치즈김치볶음밥": {"english_name": "Cheese Kimchi Fried Rice", "description": "Savory kimchi fried rice smothered under a thick layer of melted mozzarella cheese.", "spicy_level": "🌶️ (Mild)", "pork_included": "Maybe", "allergies": "Milk, Egg, Soybean, Pork"},
            "카레볶음밥": {"english_name": "Curry Fried Rice", "description": "Rice wok-tossed with aromatic curry seasoning, mixed vegetables, and scrambled eggs.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Wheat, Egg"},
            "새우볶음밥": {"english_name": "Shrimp Fried Rice", "description": "Wok-fried rice enhanced with small, plump whole shrimp and scrambled eggs.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Shrimp/Crustacean, Egg"},
            "치킨볶음밥": {"english_name": "Chicken Fried Rice", "description": "Wok-fried rice tossed with tender diced chicken pieces, mixed vegetables, and savory sauce.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Chicken, Soybean, Egg"},
            "계란후라이": {"english_name": "Fried Egg Side", "description": "A simple, perfectly cooked sunny-side-up or over-easy fried egg side dish.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "Egg"},
            "공기밥": {"english_name": "Bowl of Plain Rice", "description": "A standard individual metallic bowl of steaming hot plain white short-grain rice.", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "None"},
            "음료수": {"english_name": "Soft Drinks / Beverage", "description": "Assorted carbonated canned sodas or soft drinks (such as Cola, Sprite, or Fanta).", "spicy_level": "❌ Non-spicy", "pork_included": "❌ NO", "allergies": "None"}
        }

    def extract_and_analyze(self, binary_matrix):
        """
        Performs global block text parsing alongside line checks to ensure maximum match density.
        """
        tesseract_config = r'--oem 3 --psm 6'
        try:
            raw_string = pytesseract.image_to_string(binary_matrix, lang='kor', config=tesseract_config)
            
            # Extract standard line structure
            raw_lines = raw_string.split('\n')
            
            # Strategy 1: Create a unified global clean block (keeps spaces and line breaks)
            cleaned_text_block = re.sub(r'[^가-힣\s]', '', raw_string)
            
            # Initialize empty container for verified matches
            matched_items = []
            seen_food = set()
            
            # Double-layered resilient token evaluation
            for food_name, details in self.food_database.items():
                if food_name in seen_food:
                    continue
                    
                # Level A: Global raw block index match
                if food_name in cleaned_text_block:
                    matched_items.append({"korean_name": food_name, **details})
                    seen_food.add(food_name)
                    continue
                
                # Level B: Bounded regex character gap match (handles internal noise dots "김.밥")
                pattern = ".*".join(list(food_name))
                if re.search(pattern, cleaned_text_block):
                    matched_items.append({"korean_name": food_name, **details})
                    seen_food.add(food_name)
                    continue
                    
                # Level C: Fast line-level character density fallback
                for line in raw_lines:
                    cleaned_line = re.sub(r'[^가-힣]', '', line)
                    if len(food_name) >= 2:
                        chars_found = sum(1 for char in food_name if char in cleaned_line)
                        if chars_found >= len(food_name) - 1 and len(cleaned_line) <= len(food_name) + 3:
                            matched_items.append({"korean_name": food_name, **details})
                            seen_food.add(food_name)
                            break
                            
            return matched_items, raw_string
        except Exception as error_msg:
            return [], str(error_msg)