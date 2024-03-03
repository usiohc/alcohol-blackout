<style>

  /* container 양쪽 패딩 없애기 */
  .no-padding {
    padding-left: 0;
    padding-right: 0;
  }

  /* border 두께 조정 */
  .border-thickness {
    border-width: 1.5px !important; /* 원하는 두께로 변경 */
  }


  /* bootstrap 기본 style 재정의 */
  .nav-item .nav-link {
    font-size: 14px; 
    font-weight: 600; 
    color: #000000 !important; 
  } 

  /* active 기본 style 재정의 */
  .nav-item .nav-link.active {
    background-color: transparent;
    color: #6482B9 !important;
    border-bottom: 2px solid #6482B9;
    border-radius: 0;
  } 

  /* input(search) 박스 선택시 생기는 border 제거 */
  .no-outline:focus {
    box-shadow: none;
  }

  .navbar-brand {
    font-family: 'Bagel Fat One', system-ui;
  }

</style>

<script>
  import { link, location } from 'svelte-spa-router';
  import { selectedItems, searchQuery } from '../lib/store'; // 새로고침시 현재 경로를 추적하는 스토어
  import { access_token, email, is_login } from '../lib/store';
  import searchSvg from '../assets/search.svelte'; // 돋보기 svg
  
  $: $searchQuery;

  // 기주, 재료, 칵테일 store 초기화 함수
  function resetItems() {
    $selectedItems = {'spirits': [], 'materials': []};
    $searchQuery = '';
  }


  // 해당 함수 호출시 햄버거 메뉴 클릭 -> 축소
  let hamburgerButton;
  function toggleHamburger() {
    hamburgerButton.click();
  }

  // 로그아웃 함수
  function logout() {
    $access_token = '';
    $email = '';
    $is_login = false;
    toggleHamburger();
  }

</script>



<!-- 네비게이션바 -->
<nav class="navbar navbar-dark border-bottom" style="background-color: #6482B9">
    <div class="container-fluid">
      <a use:link class="navbar-brand" href="/" on:click={() => {}}>ACBO</a>
        <button bind:this={hamburgerButton}
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent"
                data-bs-auto-close="true"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"/>
        </button>
        <div class="collapse navbar-collapse " id="navbarSupportedContent">
          <ul class="navbar-nav">
              <!-- <li class="nav-item">
                <a use:link class="nav-link disabled" href="/" 
                style="text-decoration: line-through; color: gray !important;"
                on:click={() => { toggleHamburger();}}>게시판</a>
              </li> -->
              <li class="nav-item">
                  <a use:link class="nav-link" href="/cocktail/request" 
                  style="{$location === '/cocktail/request' ? 'color: black !important;' : 'color: white !important;'}"
                  on:click={() => { toggleHamburger();}}>칵테일 요청</a>
              </li>
              {#if $is_login}
              <li class="nav-item">
                <a use:link class="nav-link" 
                style="{$location === '/bookmark' ? 'color: black !important;' : 'color: white !important;'}"
                href="/bookmark" on:click={() => { toggleHamburger();}}>저장한 칵테일</a>
              </li>
              <li class="nav-item">
                <a use:link class="nav-link" 
                style="{$location === '/mypage' ? 'color: black !important;' : 'color: white !important;'}"
                href="/mypage" on:click={() => { toggleHamburger();}}>마이페이지</a>
              </li>
              <li class="nav-item">
                <a use:link class="nav-link" 
                style="color: white !important;"
                href="/" on:click={() => { logout();}}>로그아웃</a>
              </li>
              {:else}
              <li class="nav-item">
                  <a use:link class="nav-link" href="/login" 
                  style="{$location === '/login' ? 'color: black !important;' : 'color: white !important;'}"
                  on:click={() => { toggleHamburger();}}>로그인</a>
                  <!-- style="text-decoration: line-through; color: gray !important;" -->
              </li>
              {/if}
          </ul>
        </div>
    </div>
</nav>  

<nav class="nav sticky-top nav-fill bg-white">
  <div class="container-fluid no-padding">

    <ul class="nav nav-pills nav-justified border-bottom border-gray">
      <li class="nav-item">
        <a use:link class="nav-link {$location === '/spirit' ? 'active' : ''}" href="/spirit">기주</a>
      </li>
      <li class="nav-item">
        <a use:link class="nav-link {$location === '/material' ? 'active' : ''}" href="/material">재료</a>
      </li>
      <li class="nav-item">
        <a use:link class="nav-link {$location === '/cocktail' ? 'active' : ''}" href="/cocktail">칵테일</a>
      </li>
      <li class="nav-item">
        <a use:link class="nav-link" href="/" on:click={() => resetItems()}>초기화</a>
      </li>
    </ul>

    <div class="d-flex border-bottom border-primary border-thickness">
      <input
      class="form-control me-0 border-0 no-outline"
      type="text"
      placeholder="Search"
      aria-label="Search"
      bind:value={$searchQuery}>
      <button class="btn btn-outline-light border-0 disabled" type="button">
        <!-- 돋보기 svg -->
          <svelte:component this={searchSvg} />
      </button>
    </div>

  </div>
</nav>
  