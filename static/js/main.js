var cart = {};

const swiper = new Swiper('.swiper', {
autoplay: {
    delay: 2000,
    disableOnInteraction: false,
},
loop: true,

pagination: {
    el: '.swiper-pagination',
    clickable: true
},

navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
},
});



tailwind.config = {
    theme: {
      extend: {
        colors: {
          Canteen: '#004B93',
        }
      },
    }

  }


function AddItemToCart(pid, action='add', e=null){
  let para = $(`#qtty${pid}`);
  let cartCounter = $("#cartCounter");
  let cartInput = $("#cartInput");
  let prev_qtty;
  switch(action){
    case "add":
      cart[pid] = 1;
      para.text(1)
      break;
    case "inc":
      prev_qtty= cart[pid];
      cart[pid]= prev_qtty+1;
      para.text(prev_qtty+1)
      break;
    case "dec":
      prev_qtty = cart[pid];
      prev_qtty -= 1;
      if(prev_qtty <= 0){
        delete cart[pid];
        para.text(0)
        $(e.target).parent().parent().hide();
        $(e.target).parent().parent().siblings().fadeIn();
      }else{
        cart[pid]= prev_qtty;
        para.text(prev_qtty)
      }
      break;
  }
  cartCounter.text(Object.keys(cart).length);
  cartInput.val(JSON.stringify(cart));
}

const AddToCartButtons = document.querySelectorAll("#AddToCartButton");
AddToCartButtons.forEach((value, index)=>{  
  $(value).click((e)=>{
    let button = $(value);
    let pid = button.attr("value");
    AddItemToCart(pid)
    button.hide();
    button.siblings().fadeIn();
  });
});

const cart_plus_btn = document.querySelectorAll("#cart-plus-btn");
cart_plus_btn.forEach((input, index)=>{
  $(input).on("click", (e)=>{
    let pid =  e.target.value;
    AddItemToCart(pid, "inc", e);
  });
});

const cart_minus_btn = document.querySelectorAll("#cart-minus-btn");
cart_minus_btn.forEach((input, index)=>{
  $(input).on("click", (e)=>{
    let pid =  e.target.value;
    AddItemToCart(pid, "dec", e);
  });
});



var menu_toggle = 1;

$(".menu-btn").click(function(e) {
    const menu_li = $(".menu-items ul li");
    menu_toggle += 1;
    
    if(menu_toggle%2==0){
        $('.menu-items').animate({height:'122px'},);
        for (let li of menu_li){
            $(li).show(500);
        }
    }else{
        for (let li of menu_li){
            $(li).hide('fast');
        }
        $('.menu-items').animate({height:'0px'},);

    }
});



const OrderDetails = document.querySelectorAll("#OrderDetails");
OrderDetails.forEach((div, index)=>{
    let d = $(div);
    d.on("click", (e)=>{
      childs =d.children().siblings()[3];
      $(childs).toggleClass("h-0");
    });
});