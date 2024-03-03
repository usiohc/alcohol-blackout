<script>
  import Router from 'svelte-spa-router'
  import Navigation from "./components/Navigation.svelte"

  import Home from "./routes/Home.svelte"
  import Test from "./routes/Test/Test.svelte"
  import Spirit from "./routes/builder/Spirit.svelte"
  import Material from "./routes/builder/Material.svelte"
  import Cocktail from "./routes/builder/Cocktail.svelte"
  import CocktailDetail from "./routes/cocktail/CocktailDetail.svelte"
  import CocktailRequest from "./routes/cocktail/CocktailRequest.svelte"
  
  import Login from "./routes/user/Login.svelte"
  import Register from "./routes/user/Register.svelte"
  import MyPage from "./routes/user/MyPage.svelte"
  import Bookmark from "./routes/user/Bookmark.svelte"
  import TokenVerify from "./routes/user/TokenVerify.svelte"

  import NotFound from "./routes/NotFound.svelte"

  const routes = {
    '/': Home,
    '/spirit': Spirit,
    '/material': Material,
    '/cocktail': Cocktail,
    '/cocktail/request': CocktailRequest, // ":param" 과 같은 동적 라우팅보다 상단에 위치해야 함 
    '/cocktail/:name': CocktailDetail,

    // verify Token
    '/token/:token': TokenVerify,

    // user
    '/login': Login,
    '/register': Register,
    '/mypage': MyPage,
    '/bookmark': Bookmark,

    // Catch-all
    // This is optional, but if present it must be the last
    '*': NotFound,
  }

  if (import.meta.env.DEV) {
    routes['/test'] = Test
  } 

  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=G-T9EM5M1GGE';
  script.onload = () => {
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-T9EM5M1GGE');
  };
  document.head.appendChild(script);
  
  function routeLoaded(event) {
      // console.log('routeLoaded event')
      // // The first 5 properties are the same as for the routeLoading event
      // console.log('Route', event.detail.route)
      // console.log('Location', event.detail.location)
      // console.log('Querystring', event.detail.querystring)
      // console.log('Params', event.detail.params)
      // console.log('User data', event.detail.userData)
      // // The last two properties are unique to routeLoaded
      // console.log('Component', event.detail.component) // This is a Svelte component, so a function
      // console.log('Name', event.detail.name)
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-T9EM5M1GGE', {'page_path': event.detail.location})
  }
</script>

<Navigation />
<Router {routes} 
  on:routeLoaded={routeLoaded}
  restoreScrollState={true}/>