function setupRegionHover() {
    const regionImages = {
      Jiangnan: "/static/media/Jiangnan/gui_hua_tang_ou.png",
      Xinjiang: "/static/media/Xinjiang/big_plate_chicken.png",
      Dongbei: "/static/media/Dongbei/dumpling.png",
      Sichuan: "/static/media/Sichuan/fried_pork_kidney.png",
      Guangdong: "/static/media/Guangdong/char_siu.png"
    };
  
    let hideTimeout;
  
    $(".dot").on("mouseenter", function () {
      const $dot = $(this);
      const region = $dot.data("region");
  
      clearTimeout(hideTimeout);
  
      // Update content in the popup
      $("#region-image").attr("src", regionImages[region]);
      $("#region-name").text(region);
      $("#explore-link").attr("href", "/learn/" + region.toLowerCase());
  
      // Position and show popup
      const offsetTop = $dot.position().top;
      const offsetLeft = $dot.position().left;
      $("#region-info")
        .removeClass("hidden")
        .css({
          top: offsetTop - 90 + "px",
          left: offsetLeft + 40 + "px"
        });
    });
  
    $(".dot").on("mouseleave", function () {
      hideTimeout = setTimeout(() => {
        $("#region-info").addClass("hidden");
      }, 200);
    });
  
    $("#region-info").on("mouseenter", function () {
      clearTimeout(hideTimeout);
    });
  
    $("#region-info").on("mouseleave", function () {
      $("#region-info").addClass("hidden");
    });
}

$(document).ready(function () {
    setupRegionHover();
});