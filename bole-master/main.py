from scrapy.cmdline import execute
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy','crawl','comment'])
execute(['scrapy','crawl','qichachaapi'])
# execute(['scrapy','crawl','test'])
# def zhixing():
#
#     execute(['scrapy', 'crawl', 'qiye'])