<style>
    div {
        font-family: 'Nanum Gothic', sans-serif;
    }
</style>

<script>    
    import { onMount } from "svelte";
    import fastapi from "../../lib/api";    
    import Error from "../../components/Error.svelte";
    import Image from "../../components/Image.svelte";
    import { is_login } from "../../lib/store";

    export let params;
    
    // Material/Garnish/Lemon.jpg

    let spirit_type = {
        "Whisky": "위스키",
        "Brandy": "브랜디",
        "Gin": "진",
        "Rum": "럼",
        "Tequila": "데킬라",
        "Vodka": "보드카",
        "Liqueur": "리큐어",
        "Wine": "와인",
        "Beer": "맥주",
    }

    let material_type = {
        "Liqueur": "리큐어",
        "Juice": "주스",
        "Syrup": "시럽",
        "Soda": "소다",
        "Garnish": "가니쉬",
        "Etc": "기타",
    }

    let cocktail_skill = {
        "Build": "빌드",
        "Stir": "스터",
        "Shake": "쉐이크",
        "Float": "플로트",
        "Blend": "블랜드"
    }
    
    let material_unit = {
        "ml": "ml",
        "tsp": "tsp",
        "dash": "dash",
        "drop": "drop",
        "pinch": "꼬집",
        "Full_up": "가득",
        "piece": "개"
    }

    let cocktail = {};
    $: cocktail;

    let isBookmarked = false;
    $: isBookmarked;

    let isLoaded = false;
    let error = {detail:[]};
    let name = params.name;
    let imagePath_GCP = "https://storage.googleapis.com/acbo-images/"


    async function get_cocktail() {
        let url = '/api/cocktails/' + name;
        let params = {}
        fastapi('get', url, params, 
            (json) => { 
                cocktail = json
                // cocktail.imagePath = "/acbo-images/" + "Cocktail/" + cocktail.name + ".jpg";
                cocktail.imagePath = imagePath_GCP + "Cocktail/" + cocktail.name + ".jpg";
                cocktail.spirits.forEach(spirit => {
                    // spirit.imagePath = "/acbo-images/" + "Spirit/" + spirit.type + ".jpg";
                    spirit.imagePath = imagePath_GCP + "Spirit/" + spirit.type + ".jpg";
                });
                cocktail.materials.forEach(material => {
                    // material.imagePath = "/acbo-images/" + "Material/" + material.type + "/" + material.name + ".jpg";
                    material.imagePath = imagePath_GCP + "Material/" + material.type + "/" + material.name + ".jpg";
                });
                if ($is_login)
                    get_is_bookmarked(cocktail.id);
                isLoaded = true;
            }, 
            (json_error) => { 
                error = json_error
            }
        )
    }

    async function get_is_bookmarked(id) {
        let url = '/api/bookmarks/' + id;
        let params = {}
        fastapi('get', url, params, 
            (json) => { 
                isBookmarked = json.is_bookmarked
            }, 
            (json_error) => { 
                error = json_error
            }
        )
    }

    async function bookmark(event) {
        event.preventDefault()
        let method = ""
        if (isBookmarked) {
            method = "delete"
        } else {
            method = "post"
        } 
        let url = '/api/bookmarks/' + cocktail.id;
        let params = {}
        fastapi(method, url, params, 
            (json) => { 
                isBookmarked = !isBookmarked
            }, 
            (json_error) => { 
                error = json_error
            }
        )
    }


    onMount(() => {
        get_cocktail();
        
    })

</script>

{#if !isLoaded}
    {#if error.detail.length > 0}
        <Error error={error} />
    {:else}
    <div class="d-flex justify-content-center">
        <div class="spinner-border mt-5 p-4 text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    {/if}
{:else}

<div class="container-md text-center px-3 mt-3">
    
    <div class="shadow p-3 px-4 mb-5 rounded">
        <div class="row row-cols-1 row-cols-sm-2 text-center">
            <div class="col">
                <Image src={cocktail.imagePath} img_class="img-fluid card-img-top rounded" width="" height=""/>
            </div>
            <div class="col mt-3">
                <p class="h2">{cocktail.name_ko}</p><p class='small'>{cocktail.name}</p>
                <h4>
                    <span class="badge bg-primary">약 {cocktail.abv}도</span>
                    <span class="badge bg-primary">{cocktail_skill[cocktail.skill]} 기법</span>
                </h4>
                <!-- <h6>조회수: {cocktail.usage_count}</h6> -->
            </div>
        </div>
        <div class="row">
            {#if $is_login}
                <button on:click="{ bookmark }" class="btn {isBookmarked ? "btn-success" : "btn-outline-success"}">
                    {#if isBookmarked}
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-check" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M10.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                            <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1H4z"/>
                        </svg>
                    {:else}
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark" viewBox="0 0 16 16">
                            <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1H4z"/>
                        </svg>
                    {/if}
                    저장
                </button>
            {:else}
                <button on:click="{ bookmark }" class="btn btn-outline-success disabled">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark" viewBox="0 0 16 16">
                        <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1H4z"/>
                    </svg>
                    저장
                </button>
            {/if}
        </div>
    </div>

    <div class="card p-1 text-bg-primary">
        <div class="h4">기주</div>
    </div>
    <div class="shadow p-3 mb-5 rounded">
        {#each cocktail.spirits as {imagePath, type, amount, unit, name, name_ko}}
        <div class="row g-3 row-cols-3 align-items-center">
            <div class="col-2">
              <Image src={imagePath} img_class="img-fluid rounded card-img-top" width="" height=""/>
            </div>
            {#if name_ko}
                <div class="col-1"></div>
                <div class="col-3"><p class="text-start">{spirit_type[type]}</p></div>
                <div class="col-4"><p class="text-start">{name_ko}</p></div>
                    <!-- <small class="text-body-secondary">{name}</small></div> -->
            {:else}
                <div class="col-8">{spirit_type[type]}</div>
            {/if}
            <div class="col-2"><p class="text-end">{amount}{unit}</p></div> 
        </div>
        {/each}
    </div>

    <div class="card p-1 text-bg-primary">
        <div class="h4">재료</div>
    </div>
    <div class="shadow p-3 mb-5 rounded">        
        {#each cocktail.materials as {imagePath, type, name, name_ko, amount, unit}}
        <div class="row g-2 row-cols-3 align-items-center">
                <div class="col-2">
                    <Image src={imagePath} img_class="img-fluid rounded card-img-top" width="" height=""/>
                </div>
                <div class="col-1"></div>
                <div class="col-3"><p class="text-start">{material_type[type]}</p></div>
                <div class="col-{unit==="Full_up" ? "3" : "4"}"><p class="text-start">{name_ko}<br>
                    <!-- <small>{name}</small> -->
                </p></div>
                <div class="col-{unit==="Full_up" ? "3" : "2"} text-end"><p class="text-end">{amount? amount : ''}{material_unit[unit]}</p></div>
            </div>
        {/each}
    </div>
</div>


{/if}