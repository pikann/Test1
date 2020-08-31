# Test1
Phần mềm crawl data trên website https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page=1&per_page=30

### Cài đặt
Cài đặt thư viện:
```
$ pip install requests
$ pip install beautifulsoup4
```
Chạy chương trình:
```
$ python Main.py
```
### Dữ liệu đầu ra
File data.json có dạng:
```
 ___title (Title Book)
|
 ___link (Link Book)
|
 ___id (ID Book)
|
 ___author (Author Book)
|
 ___rate (Rate Book)
|
 ___description (Description Book)
|
 ___review (Reviews Book)
      |
       ___id (ID User)
      |
       ___name (Name User)
      |
       ___rate (Rate)
      |
       ___date (Date post)
      |
       ___content (Review content)
      |
       ___list_cmt (List comments)
            |
             ___name (Name User)
            |
             ___id (ID User)
            |
             ___date (Date post)
            |
             ___cmt (Comment)
```
