// 獲取searchForm和page-link
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

// 確保searchForm存在
if(searchForm){
    for (let i=0; pageLinks.length > i; i++){
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault() // 預防預設操作

            // 獲取資料屬性
            let page = this.dataset.page

            // 加入隱藏搜索<input>標籤到表單中
            searchForm.innerHTML += `<input value=${page} name="page" hidden>`

            // Submit表單
            searchForm.submit()
        })
    }
}