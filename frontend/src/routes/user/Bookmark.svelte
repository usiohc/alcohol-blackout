<script>
    import { onMount } from "svelte";
    import { push } from "svelte-spa-router";
    import fastapi from "../../lib/api"
    import Error from "../../components/Error.svelte"
    import Image from "../../components/Image.svelte";


    let error = {detail:[]};
    let cocktails = []
    let total = 0;
    const imagePath_GCP = "https://storage.googleapis.com/acbo-images/"
    
    async function get_bookmark_cocktail_list() {
        let url = '/api/bookmarks'
        let params = {}
        fastapi('get', url, params, 
            (json) => { 
                total = json.total
                cocktails = json.items
                cocktails.forEach(cocktail => {
                    cocktail.imagePath = imagePath_GCP + "Cocktail/" + cocktail.name + ".jpg";
                });
            },
            (json_error) => { 
                error = json_error
            }
        )
    }

    function toggleCard(name) {
        push('/cocktail/' + name)
    }

    onMount(() => {
        get_bookmark_cocktail_list();
    })



</script>


<div class="px-3">
    <div class="text-center mt-3">
      <p>검색된 칵테일 수 : { cocktails.length }</p>
    </div>
    <Error error={error} margin="mt-3"/>
    <div class="row row-cols-2 row row-cols-xs-2 row-cols-sm-3 row-cols-md-3 row-cols-lg-4 g-3">
      {#each cocktails as { name, name_ko, usage_count, imagePath }}
        <div class="col">
          <button on:click="{ toggleCard(name) }" style="background: none; border: none; padding: 0; cursor: pointer;">
            <div class="card shadow-sm">
              <div class="" style="min-width: 162.35px; min-height: 162.35px;">
                <Image src={imagePath} img_class="img-fluid rounded card-img-top" width="100%" height="100%"/>
              </div>
              <div class="card-body"  style="text-align: center;">
                <p class="card-text">{name_ko}<br>
                <small class="text-body-secondary">{name}</small></p>
              </div>
            </div>
          </button>
        </div>
      {/each}
    </div>
  </div>