dtable = new webix.ui({
    container:"browsetable",
    id:"dtable",
    view:"datatable",
    columns:[
        { id:"uniprot", map:"#data1#", header:["UniProt AC", {content:"textFilter"}], adjust:true},
        { id:"genename", map:"#data2#", header:["Gene name", {content:"textFilter"}], adjust:true},
        { id:"locus", map:"#data3#", header:["Locus", {content:"textFilter"}], adjust:true},
        // { id:"strain", map:"#data4#", header:["Strain", {content:"selectFilter"}], fillspace:true},
        { id:"numort", map:"#data5#", header:"Othologs", adjust:true},
        { id:"numint", map:"#data6#", header:"Interactions", adjust:true}
    ],
    resizeColumn:true,
    datatype:"csv",
    url:'data/nodes.csv',
    autoheight:true,
    // autowidth:true,
    pager: {
        template: "{common.prev()}{common.next()}Page {common.page()} from #limit#",
        container: "paging_here",
        size: 15,
        group: 5
    },
    hover:"browse_row_hover",
            on:{
                "onItemClick":function(id, e, trg){
                    //window.location.href = "proteins/"+dtable.getItem(id.row).uniprot+".html";
                    window.location.href = "uniprot.html";
                    //webix.message("Click on row: "+dtable.getItem(id.row).uniprot);
                }
    }
});
var strain_select = [{
    view:"select",
    name: "strain",
    label:"Select strain",
    options:[
        "data/nodes1.csv",
        "data/nodes2.csv",
        "data/nodes3.csv"
    ]
}];
strain_select_form = new webix.ui({
    container:"strain_select_div",
    id: "strain_select_form",
    view:"form",
    scroll:false,
    width:300,
    elements: strain_select
});
$$("strain_select_form").elements["strain"].attachEvent("onChange", function(newv, oldv){
    dtable.clearAll()
    dtable.url=newv;
    dtable.load(newv);
    $$("dtable").refresh();
    webix.message("Value changed from: "+oldv+" to: "+newv);
});