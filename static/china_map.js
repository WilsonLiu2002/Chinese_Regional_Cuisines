function setupRegionHover() {
  let hideTimeout;

  $(".dot").on("mouseenter", function () {
    const $dot = $(this);
    const region = $dot.data("region");

    clearTimeout(hideTimeout);

    // — NEW: dish image
    $("#dish-image")
      .attr("src", regionImages[region]   || '/static/media/placeholder_dish.png');

    // — UPDATED: region snapshot
    $("#region-image")
      .attr("src", regionPics[region]     || '/static/media/placeholder_region.png');

    // — NEW: outfit image
    $("#outfit-image")
      .attr("src", outfitImages[region]   || '/static/media/placeholder_outfit.png');


    $("#region-name").text(region);
    $("#explore-link").attr("href", "/learn_culture/" + region.toLowerCase());

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