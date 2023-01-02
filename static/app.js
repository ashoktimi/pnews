const BASE_URL = "https://qnewsapp.herokuapp.com";
// const BASE_URL = "http://127.0.0.1:5000";

$(document).on('click', '#iBtn', function(e){ 
  e.preventDefault(); 
  location.assign(`${BASE_URL}`);
});


// make article favorite and remove favorite 
$(document).on('click', '.makefavorite', function(e){ 
  e.preventDefault(); 
  const id = $(this).data('id') 
  location.assign(`${BASE_URL}/favorites/articles/${id}`);  
});

// get the search form when click on search icon
$(document).on('click', '#searchBtn', function(e){ 
  e.preventDefault(); 
  location.assign(`${BASE_URL}/search`);  
});


// Search for article with query parameters

$(document).ready(function(){  
$("#filterForm").submit(function(e){
  e.preventDefault();  
  let searchvalue = $("#searchtext").val(); 
  let searchfrom = $("#fromvalue").val();
  let searchto = $("#tovalue").val();

  console.log(searchvalue, searchfrom, searchto)

  $(".maincontent").remove();  
  if(
    ![false, 0, "", null, undefined, NaN].includes(searchfrom) 
    && 
    ![false, 0, "", null, undefined, NaN].includes(searchto)
    ) {
    let url = `${BASE_URL}/api/get_articles/${searchvalue}/${searchfrom}/${searchto}`
    addArticle(url)
    }else{
    let url = `${BASE_URL}/api/get_articles/${searchvalue}`
    addArticle(url)  
  }
});
})


$('#sortid').change(handleSelect);
function handleSelect(ev) {
  ev.preventDefault()
  let select = ev.target;
    $("#myForm").submit(function(e){
      e.preventDefault();  
      let searchvalue = $("#searchtext").val();
      let sortvalue = select.value
      console.log(searchvalue, sortvalue)
        $(".maincontent").remove();
        let url = `${BASE_URL}/api/get_articles/${searchvalue}/${sortvalue}`
        addArticle(url) 
   }
)}


function addArticle(url){
  $(".container").append(generatePageHTML)
  axios.get(url)
          .then( res => {
            res.data.articles.forEach( r => $(".container").append(
              `
              <div class="col-sm-6 col-xl-4 maincard">
                <div class="card">
                  <img src="${r.urlToImage}" class="card-img-top" alt=""> 
                    <div class="card-body">
                      <a class="card-text cardclass" href="${r.url}">
                        <p class="titleclass" >${r.title}</p>
                      </a>
                      <small>${r.description}</small>
                      _
                      <h10>${r.author}</h10>   
                      <button type="button" class="btn btn-light btn-sm favoriteaddarticle" 
                        data-url=${r.url} data-img_url=${r.urlToImage} data-pub_data=${r.publishedAt}> 
                        <img src='/static/images/makefavorite.png' style="width: 1.5rem; height: 1.5rem;" alt="submit form">
                      </button>                     
                    </div>
                </div>        
              </div> 
            `
            )  
          )
      })
    }

function generatePageHTML() {
    return `
    <style>
      body{background-color:rgb(194, 226, 238);}
    </style>
      <nav class="navbar navbar-dark bg-dark" >
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggleExternalContent" 
              aria-controls="navbarToggleExternalContent" 
              aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
          </button>
          <a href="/" class="iBtn">Pnews</a>
          <ul class="nav-ul" >         
            <li class="nav-li"><a href="/search"><span class="fa fa-search" id="searchBtn"></span></a></li>
            <li class="nav-li"><a href="/article" class="nav-anchor">Articles</a></li>              
          </ul>
      </nav>      
      <div class="row searchRowcolor">
        <div class="col-12 col-sm-6 col-xl-4 bg-danger barHeight"></div>
        <div class="col-12 col-sm-6 col-xl-4 bg-info barHeight"></div>
        <div class="col-12 col-sm-6 col-xl-4 bg-warning barHeight"></div>
    </div> 
    `
  }


$(document).on('click', '.categoryBtn',   function(e){ 
  e.preventDefault();  
  $(".maincontent").remove();
  $(".container").empty();
  let categoryvalue = $(this).data('name')
  let url = `${BASE_URL}/api/cat_articles/${categoryvalue}`
  showArticle(url, categoryvalue)  
});

function showArticle(url, category){
  $(".container").append(generateSourceHTML(category))
 axios.get(url)
  .then( res => {
        res.data.sources.forEach( r => $(".container").append(
      `
      <div class="col-sm-6 col-xl-4 style="margin-top:1rem;"">
        <div class="card">
          <div class="card-body">
            <a class="card-text cardclass" href="${r.url}">
              <p class="titleclass" >${r.name}</p>
            </a>
            <small>${r.description}</small>                    
          </div>
        </div>        
      </div> 
      `
    ))
  })
}



function generateSourceHTML(category) {  
  return `
  <style>
    body{background-color:rgb(194, 226, 238);}
  </style>
    <nav class="navbar navbar-dark bg-dark" style="display:flex; justify-content:space-around;">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggleExternalContent" 
            aria-controls="navbarToggleExternalContent" 
            aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <a href="/" class="iBtn">Pnews</a>
        <ul class="nav-ul" style="width:80%">        
          <button type="button" class="btn btn-link categoryBtn" data-name="general" > General</button>
          <button type="button" class="btn btn-link categoryBtn" data-name="science" >Science</button>
          <button type="button" class="btn btn-link categoryBtn" data-name="technology" >Technology</button>
          <button type="button" class="btn btn-link categoryBtn" data-name="health" >Health</button>
          <button type="button" class="btn btn-link categoryBtn" data-name="entertainment" >Entertainment</button>
          <button type="button" class="btn btn-link categoryBtn" data-name="sports" >Sports</button>
          <button type="button" class="btn btn-link categoryBtn" data-name="business" >Business</button>            
        </ul>
    </nav> 
  <h3 class="cat-source"> ${category} </h3>  
    <div class="row searchRowcolor">
      <div class="col-12 col-sm-6 col-xl-4 bg-danger barHeight"></div>
      <div class="col-12 col-sm-6 col-xl-4 bg-info barHeight"></div>
      <div class="col-12 col-sm-6 col-xl-4 bg-warning barHeight"></div>
    </div> 
  `
}


// add article to the articles table and so to the articles_categories;

$(document).on('click', '.favoriteaddarticle', async function(e){ 
  e.preventDefault(); 
  const url = $(this).data('url')
  const Image_URL = $(this).data('img_url')
  const published_date = $(this).data('pub_data')
  const card = document.querySelectorAll(".cardclass")
  for (i=0; i<card.length; i++){
    if (url == card[i].href){
    let title = card[i].innerText
    let div = card[i].parentElement
    let c = div.innerText  
    let ct = c.slice(title.length)
    let author = ct.split('_')[1]
    let description = ct.replace(author,'').replace('_','')
    return await axios.post(`${BASE_URL}/api/categories/articles`, {
      author,
      title,
      description,
      url,
      Image_URL,
      published_date
    })

  }}
})















