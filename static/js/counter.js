function postData(stts, pid){
    $(`#row${pid}`).fadeOut();
    $.post(`../../counter/setstatus/${stts}/`, data={"pid":pid},(data, status, xhr)=>{
            if(status == "failed"){
                alert("we faced an error");
            }else{
            }
        }, dataType="json");
}


document.querySelectorAll("#AcceptOrder").forEach((btn, index)=>{
    $(btn).on("click",(e)=>{
        postData("accepted", e.target.value);
    });
});

document.querySelectorAll("#RejectOrder").forEach((btn, index)=>{
    $(btn).on("click",(e)=>{
        postData("rejected", e.target.value);
    });
});



document.querySelectorAll("#MarkAsRejected").forEach((btn, index)=>{
    $(btn).on("click",(e)=>{
        postData("rejected", e.target.value);
    });
});




document.querySelectorAll("#MarkAsDelivered").forEach((btn, index)=>{
    $(btn).on("click",(e)=>{
        postData("completed", e.target.value);
    });
});


document.querySelectorAll("#copy_address_details").forEach((btn, index)=>{
    $(btn).on("click",(e)=>{
        CopyToClipBoard(e.target.value);
        e.target.innerHTML = 'Copied'
    });
});

function CopyToClipBoard(id){
    let a = `
Name: ${$(`#order-details-name_${id}`).text()}
Phone: ${ $(`#order-details-phone_${id}`).text() }
Address:  ${ $(`#order-details-address_${id}`).text() }

Order id: ${ $(`#order-details-orderid_${id}`).val() }
Payment method: ${ $(`#order-details-payment-method_${id}`).val() }

Amount : ${ $(`#order-details-amount_${id}`).val() }
Items : ${ $(`#order-details-items_${id}`).text() }

`;
    navigator.clipboard.writeText(a);
}



  
  $(document).ready(function() {
    const interval = setInterval(function() {
        $.ajax({
            url: '/counter/notification/',
            method:"GET",
            success: function(data) {
                
                if(data.status == "ok") {
                    const audio = new Audio("../../static/media/notify.wav");
                    audio.play();
                    data.data.forEach((value, i) => {
        
                    const s = `
                            <tr class="hover:bg-slate-200 rounded p-2" id="row${value.id}">
                                <td>${value.name}</td>
                                <td>${value.number}</td>
                                <td>${value.address}</td>
                                <td>${value.amount} Rs</td>
                                <td>${value.itemxqtty}</td>
                                
                                <td>
                                    <span class="text-white text-xs pb-1 px-2 rounded-md bg-rose-500"> ${value.status}</span>
                                </td>
                                <td>${value.txn_status}</td>
                                <td>${value.placed_at}</td>
        
                                <td>
                                    <button class="px-2 text-sm py-1  bg-rose-500 rounded text-white" value="${value.id}" id="RejectOrder">Reject</button>
                                    <button class="px-2 text-sm py-1  bg-emerald-500 rounded text-white" value="${value.id}" id="AcceptOrder">Accept</button>
                                </td>
                            </tr>
                        `;
                        
        
                        $("#productTable").append(s);
                    });
                }
            }
        });
    
    },20000);
   


});