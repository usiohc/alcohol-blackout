<script>
  import { onMount } from 'svelte';
  import { selectedItems, searchQuery } from '../../lib/store';
  import { search } from '../../lib/search';
  import Image from "../../components/Image.svelte";

  let spirits = [];
  let filteredSpirits;
  let isLoaded = false;
  $: isLoaded;


  async function getSpiritCard() {
    const spiritdata = {
      "Vodka": "보드카",
      "Gin":  "진",
      "Rum":  "럼",
      "Tequila":  "데킬라",
      "Whisky": "위스키",
      "Brandy": "브랜디",
      // "Liqueur": "리큐어",
      // "Beer": "맥주",
      "Wine":  "와인"
    }

    spirits = Object.entries(spiritdata).map(([name, name_ko]) => ({
      name,
      name_ko,
      imagePath: `img/Spirit/${name}.png`,
      selected: $selectedItems['spirits'].includes(name)
    }));
    filteredSpirits = spirits
    await sortCard();
    isLoaded = true;
  }
  
  async function sortCard() {
    // 선택된 카드를 먼저 보여주도록 spirits 배열을 정렬
    spirits.sort((a, b) => b.selected - a.selected);
  }
  
  // 카드를 클릭할 때마다 선택 상태를 토글하는 함수
  function toggleCard(name) {
    // spirits 배열에서 key에 해당하는 카드를 찾아서 selected 값을 반전
    const cardIndex = spirits.findIndex(card => card.name === name);
    spirits[cardIndex].selected = !spirits[cardIndex].selected;
    
    // selectedSpirits 스토어에 현재 selected=true 카드의 key만 배열로 저장
    $selectedItems['spirits'] = spirits.filter(card => card.selected).map(card => card.name);
  }

  $: {
    isLoaded = false;
    filteredSpirits = search($searchQuery, spirits);
    isLoaded = true;
  }

  onMount(() => {
    getSpiritCard();
  })

  </script>

{#if !isLoaded}
  <div class="d-flex justify-content-center">
    <div class="spinner-border mt-5 p-4 text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
{:else}
<div class="px-3">
  <div class="row row-cols-2 row row-cols-xs-2 row-cols-sm-3 row-cols-md-3 row-cols-lg-4 g-3">
    {#each filteredSpirits as { name, name_ko, imagePath, selected }}
      <div class="col">
        <button on:click={() => toggleCard(name)} style="background: none; border: none; padding: 0; cursor: pointer;">
          <div class="card shadow-sm" style={selected ? 'background-color: #ddd;' : ''}>
            <div class="" style="min-width: 162.35px; min-height: 162.35px;">
              <Image src={imagePath} img_class="img-fluid rounded card-img-top" width="100%" height="100%"/>
            </div>
            <div class="card-body"  style="text-align: center;">
              <p class="card-text">{name_ko}<sup>{name}</sup></p>
            </div>
          </div>
        </button>
      </div>
    {/each}
  </div>
</div>
{/if}