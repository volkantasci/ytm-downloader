import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class MusicScraper:
    def __init__(self, headless=True):
        self.options = ChromeOptions()
        self.options.binary_location = "/usr/bin/chromium"
        if headless:
            self.options.add_argument("--headless=new") # Modern headless
        self.options.add_argument("--lang=en-US")
        self.options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver
        try:
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                options=self.options
            )
        except:
             # Fallback
             self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.options
            )

    def get_artist_albums(self, artist_url, artist_name=None):
        """
        Scrapes the artist page to find all albums using DOM selectors.
        If artist_name is provided, uses search navigation.
        """
        # Warm up
        print("DEBUG: Warming up with home page...")
        self.driver.get("https://music.youtube.com")
        time.sleep(3)
        self._handle_popups()
        
        if artist_name:
            print(f"DEBUG: Searching for artist '{artist_name}'...")
        if artist_name:
            print(f"DEBUG: Searching for artist '{artist_name}'...")
            try:
                # Direct navigation to search query to avoid UI interaction flakiness
                from urllib.parse import quote
                # Force English for consistent "Albums" title match
                search_url = f"https://music.youtube.com/search?q={quote(artist_name)}&hl=en"
                self.driver.get(search_url)
                
                time.sleep(3)
                self._handle_popups()
                
                # Wait for results
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "ytmusic-responsive-list-item-renderer"))
                )
                
                results = self.driver.find_elements(By.TAG_NAME, "ytmusic-responsive-list-item-renderer")
                for res in results:
                     # Check if it is an artist
                     # Can check the secondary text or icon?
                     # Try to click the first one.
                     print("DEBUG: Clicking first result...")
                     
                     # Find the link inside the renderer
                     try:
                         link = res.find_element(By.TAG_NAME, "a")
                         self.driver.execute_script("arguments[0].click();", link)
                     except:
                         # Fallback to clicking element itself
                         self.driver.execute_script("arguments[0].click();", res)
                     
                     break
                
                time.sleep(5) # Wait for navigation
                self._handle_popups()
                print(f"DEBUG: Post-search URL: {self.driver.current_url}")
                print(f"DEBUG: Page Title: {self.driver.title}")
                
                # Check if we landed on a song/video page instead of artist page
                if "watch?v=" in self.driver.current_url:
                    print("DEBUG: Landed on a song page. Trying to find artist link...")
                    # Artist link is usually under the video title or in metadata
                    try:
                        # Common selector for artist name in video player UI
                        # .yt-simple-endpoint.style-scope.yt-formatted-string[href*='channel'] or similar
                        # But simpler: look for by-line
                        
                        # Wait for secondary info
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "ytmusic-player-bar"))
                        )
                        
                        # Just grab any link with 'channel' or 'browse' that has the artist name text?
                        # Or look for the specific "By Artist" element.
                        
                        # Let's try finding the owner badge
                        artist_link = self.driver.find_element(By.CSS_SELECTOR, ".byline.style-scope.ytmusic-player-bar a")
                        if artist_link:
                            print(f"DEBUG: Found artist link on song page: {artist_link.get_attribute('href')}")
                            self.driver.execute_script("arguments[0].click();", artist_link)
                            time.sleep(3)
                            self._handle_popups()
                            print(f"DEBUG: Redirected URL: {self.driver.current_url}")
                    except Exception as e:
                        print(f"DEBUG: Could not redirect from song page: {e}")
                        # If we can't find it, we might be stuck.
                
                # Now we should be on the artist page.
                
            except Exception as e:
                print(f"DEBUG: Search failed: {e}")
                self.driver.save_screenshot("debug_search_fail.png")
                return []
        else:
            print(f"Scraping {artist_url} with Selenium...")
            self.driver.get(artist_url)
        
        album_urls = set()

        try:
            # 1. Wait for main layout
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "ytmusic-app-layout"))
                )
            except TimeoutException:
                print("DEBUG: Timeout waiting for layout. Page might be blank.")
                self.driver.save_screenshot("debug_timeout.png")
                return []

            time.sleep(3) # Initial buffer
            self._handle_popups()

            # 2. Check if we need to click "Albums" -> "More"
            # Selector from browser subagent: ytmusic-shelf-renderer:has(h2 yt-formatted-string[title='Albums'])
            # We look for the Shelf with title "Albums"
            
            # Scroll down to load lazy shelves
            print("DEBUG: Scrolling to load lazy content...")
            self._scroll_page()
            
            # Find all shelves (carousel or normal)
            shelves = self.driver.find_elements(By.CSS_SELECTOR, "ytmusic-carousel-shelf-renderer, ytmusic-shelf-renderer")
            albums_shelf = None
            
            for shelf in shelves:
                try:
                    title_el = shelf.find_element(By.CSS_SELECTOR, "h2.title yt-formatted-string")
                    title_text = title_el.text.strip()
                    # Check for English or Turkish or loose match
                    if title_text in ["Albums", "Albümler", "Singles", "Tekliler"] or "Album" in title_text:
                        print(f"Found 'Albums' shelf: {title_text}")
                        albums_shelf = shelf
                        break
                except (NoSuchElementException, Exception):
                    continue
            
            if albums_shelf:
                # Check for "More" button
                try:
                    more_btn = albums_shelf.find_element(By.CSS_SELECTOR, ".more-button")
                    if more_btn.is_displayed():
                        print("Found 'More' button. Clicking...")
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", more_btn)
                        time.sleep(1)
                        more_btn.click()
                        time.sleep(3)
                        self._scroll_page()
                        self._scrape_grid_items(album_urls)
                        return list(album_urls)
                except NoSuchElementException:
                    print("No 'More' button found, scraping carousel items directly.")
                    items = albums_shelf.find_elements(By.TAG_NAME, "ytmusic-two-row-item-renderer")
                    for item in items:
                        self._extract_url_from_renderer(item, album_urls)
            
            # Fallback for direct page scraping if specific shelf logic didn't return
            if not album_urls:
                 print("Scanning page for all album links...")
                 self._scrape_grid_items(album_urls)
            
            # If still 0 items and we are on a /channel/ URL, try /browse/
            if not album_urls and artist_url and "/channel/" in artist_url:
                print("No items found on /channel/ URL. Retrying with /browse/ variant...")
                browse_url = artist_url.replace("/channel/", "/browse/")
                self.driver.get(browse_url)
                time.sleep(3)
                self._handle_popups()
                self._scrape_grid_items(album_urls)

        except Exception as e:
            print(f"Error during scraping: {e}")
            self.driver.save_screenshot("debug_error.png")
        
        return list(album_urls)

    def _scrape_grid_items(self, url_set):
        """Scrapes ytmusic-two-row-item-renderer elements from the current view."""
        items = self.driver.find_elements(By.TAG_NAME, "ytmusic-two-row-item-renderer")
        print(f"DEBUG: Found {len(items)} items in grid/list.")
        for item in items:
            self._extract_url_from_renderer(item, url_set)

    def _extract_url_from_renderer(self, item, url_set):
        try:
            # Look for the link
            # Browser subagent: a.image-wrapper or .title-column a
            links = item.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and ("browse/MPREb" in href or "playlist?list=OL" in href):
                    # print(f"DEBUG: Found URL: {href}")
                    url_set.add(href)
        except:
            pass

    def _handle_popups(self):
        # Dismiss "Install YouTube Music" or generic consent
        # Selector suggestions: caption or aria-label="Dismiss"
        try:
             # Heuristic for "No thanks" buttons
             buttons = self.driver.find_elements(By.TAG_NAME, "button")
             for btn in buttons:
                 text = btn.text.lower()
                 if "no thanks" in text or "reject" in text or "dismiss" in text:
                     btn.click()
                     time.sleep(1)
        except:
            pass

    def _scroll_page(self):
        """Scrolls to the bottom of the page to load lazy content."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(5): # Limit scroll to avoid infinite loops
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_search_results(self, query):
        """
        Searches for a query and returns the first result, prioritizing Albums.
        Returns: (url, type) where type is 'album' or 'song' or None
        """
        print(f"DEBUG: Searching for '{query}'...")
        from urllib.parse import quote
        
        # Search URL
        search_url = f"https://music.youtube.com/search?q={quote(query)}&hl=en"
        self.driver.get(search_url)
        time.sleep(3)
        self._handle_popups()
        
        try:
            # Wait for any results
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "ytmusic-shelf-renderer"))
            )
        except TimeoutException:
            print("DEBUG: No results found or timeout.")
            return None, None

        # Look for shelves
        shelves = self.driver.find_elements(By.TAG_NAME, "ytmusic-shelf-renderer")
        
        album_url = None
        song_url = None
        
        for shelf in shelves:
            try:
                title_el = shelf.find_element(By.CSS_SELECTOR, "h2.title yt-formatted-string")
                title_text = title_el.text.strip().lower()
                
                # Check for "Albums"
                if "albums" in title_text or "albümler" in title_text:
                    print("DEBUG: Found Albums section.")
                    # Get first item
                    items = shelf.find_elements(By.TAG_NAME, "ytmusic-responsive-list-item-renderer")
                    if items:
                         # Link is usually in the first 'a' tag inside 'div.title-column' or similar
                         # Let's try to find 'a' with href containing 'browse'
                         links = items[0].find_elements(By.TAG_NAME, "a")
                         for link in links:
                             href = link.get_attribute("href")
                             if href and "browse" in href:
                                 album_url = href
                                 break
                    if album_url: break

                # Check for "Songs" (only if we haven't found an album yet? Or keep looking?)
                # We prioritize albums, so we can save song url as fallback.
                if ("songs" in title_text or "şarkılar" in title_text) and not song_url:
                    print("DEBUG: Found Songs section.")
                    items = shelf.find_elements(By.TAG_NAME, "ytmusic-responsive-list-item-renderer")
                    if items:
                         # Song links usually contain 'watch'
                         links = items[0].find_elements(By.TAG_NAME, "a")
                         for link in links:
                             href = link.get_attribute("href")
                             if href and "watch" in href:
                                 song_url = href
                                 break
            except:
                continue
        
        if album_url:
            print(f"DEBUG: Selected Album URL: {album_url}")
            return album_url, 'album'
        elif song_url:
            print(f"DEBUG: Selected Song URL: {song_url}")
            return song_url, 'song'
        
        # If specific shelves not found, try "Top result" logic?
        # For now, let's return None if strict sections aren't found, OR check the top result.
        
        print("DEBUG: No specific Album or Song section found. Checking Top Result...")
        try:
             # Top result usually in 'ytmusic-card-shelf-renderer'
             card = self.driver.find_element(By.TAG_NAME, "ytmusic-card-shelf-renderer")
             title = card.find_element(By.CLASS_NAME, "title").text.lower()
             print(f"DEBUG: Top result is '{title}'")
             
             # Extract link
             link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
             
             # Extract link
             link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
             
             if "watch" in link:
                 print(f"DEBUG: Top result is a Song based on URL.")
                 return link, 'song'
             elif "browse" in link and "channel" not in link:
                 # It might be an album or artist. 
                 # Albums often have MPREb or OLAK
                 print(f"DEBUG: Top result is likely an Album based on URL.")
                 return link, 'album'
             
             # If "album" or "song" text was in title, fallback to that (though link is better)
             if "album" in title or "albüm" in title:
                  return link, 'album'
             elif "song" in title or "şarkı" in title:
                  return link, 'song'
             
        except:
            pass

        return None, None

    def close(self):
        self.driver.quit()
