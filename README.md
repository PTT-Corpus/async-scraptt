# **async-ptt-crawler**

This project scrapes/crawls post content and comments from [PTT](https://term.ptt.cc/) website, and implements [neural CKIP Chinese NLP tools](https://github.com/ckiplab/ckip-transformers) on the scraped data asynchronously.

## **Documentation**
### 1. Installation

1. Python version
   * `python == 3.7.5`

2. Clone repository

    ```bash
    git clone git@github.com:PTT-Corpus/async-scraptt.git
    ```

3. Install Requirement
    ```bash
    cd async-scraptt && pip install -r requirement.txt      
    ```

### 2. Usage

1. commands
```
scrapy crawl <spider-name> -a boards=BOARDS [-a all=True] [-a index_from=NUMBER -a index_to=NUMBER] [-a since=YEAR] [-a data_dir=PATH]

positional arguments:
<spider-name>           the name of ptt spiders (i.e. boards, ptt_post, and ptt_post_segmentation)
-a boards=BOARDS        specify which ptt boards
```

## Contact
If you have any suggestion or question, please do not hesitate to email me at philcoke35@gmail.com