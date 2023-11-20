# 동영상 기본 정보 관련
e_title = '//*[@id="title"]/h1/yt-formatted-string'
e_user = '//*[@id="text"]/a'
e_expended = '//*[@id="expand"]'
e_content = '//*[@id="description-inline-expander"]/yt-attributed-string/span/span[1]'
e_keyword = '//*[@id="info"]/a'

# 광고 관련
e_ad_title = '//div[@class="ytp-ad-text ytp-flyout-cta-headline"]'

# 연관 영상
e_related_links = '//a[@class="yt-simple-endpoint style-scope ytd-compact-video-renderer"]'

# 검색 관련
e_search_box = '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox'
e_delete_btn = '//*[@id="search-clear-button"]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]'
e_title_to_click = '//*[@id="video-title"]'