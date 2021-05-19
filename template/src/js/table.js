$(function () {
    dtable = new webix.ui({
        container: "browsetable",
        id: "dtable",
        view: "datatable",
        css:"salmonet_table protein_link",
        columns: [
            {id: "uniprot", map: "#data1#", header: ["OMA identifier", {content: "textFilter"}], width: 150},
            {id: "genename", map: "#data2#", header: ["Gene name/Locus tag (old)", {content: "textFilter"}], width: 250},
            {id: "locus_pld", map: "#data4#", header: ["Locus tag (old)", {content: "textFilter"}], width: 250},
            {id: "locus", map: "#data3#", header: ["Locus tag (new)", {content: "textFilter"}], width: 250},
            {id: "numort", map: "#data5#", header: ["Number of","Homologs"], width: 150},
            {id: "numint", map: "#data6#", header: ["Number of","Interactions"], width: 150}
        ],
        resizeColumn: true,
        datatype: "csv",
        url: data_url_prefix+'data/nodes.csv',
        autoheight: true,
        autowidth: true,
        pager: {
            css:"salmonet_table",
            template: "{common.prev()}{common.next()}Page {common.page()} from #limit#",
            container: "paging_here",
            size: 25,
            group: 5
        },
        hover: "browse_row_hover",
        on: {
            "onItemClick": function (id, e, trg) {
                window.location.href = data_url_prefix+"protein/"+dtable.getItem(id.row).uniprot.toLowerCase()+"/";
                // window.location.href = "uniprot.html";
                //webix.message("Click on row: "+dtable.getItem(id.row).uniprot);
            }
        }
    });
    webix.extend($$("dtable"), webix.ProgressBar);
    var strain_select = [
        {view: "label", label: "Select a <i>Salmonella enterica</i> strain:"},
        {
            view: "select",
            name: "strain",
            options: data_url_prefix+"data/strain_select.json"
        }];
    strain_select_form = new webix.ui({
        css:"salmonet_form",
        container: "strain_select_div",
        id: "strain_select_form",
        view: "form",
        scroll: false,
        width: 300,
        elements: strain_select
    });
    $$("strain_select_form").elements["strain"].attachEvent("onChange", function (newv, oldv) {
        $$("dtable").showProgress({
            type: "bottom",
            delay: 3000,
            hide: true
        });
        dtable.clearAll();
        dtable.load(data_url_prefix+"data/nodes" + newv + ".csv");
        $$("dtable").refresh();
        // webix.message("Value changed from: "+oldv+" to: "+newv);
    });
    $(window).resize(function() {
        if ($(window).width() < 1050){
            dtable.hideColumn("numort");
            dtable.hideColumn("numint");
        }
        if ($(window).width() >= 1050){
            dtable.showColumn("numort");
            dtable.showColumn("numint");
        }
        if ($(window).width() < 850){
            dtable.setColumnWidth("uniprot", 80);
            dtable.setColumnWidth("genename", 120);
            dtable.setColumnWidth("locus", 120);
        }
        if ($(window).width() >= 850){
            dtable.setColumnWidth("uniprot", 150);
            dtable.setColumnWidth("genename", 250);
            dtable.setColumnWidth("locus", 250);
        }
    });
    if ($(window).width() < 1050){
        dtable.hideColumn("numort");
        dtable.hideColumn("numint");
    }
    if ($(window).width() < 850){
        dtable.setColumnWidth("uniprot", 80);
        dtable.setColumnWidth("genename", 120);
        dtable.setColumnWidth("locus", 120);
    }
    // protein page
    // interactiontable = webix.ui({
    //     container: "interactiontable",
    //     view: "datatable",
    //     columns: [
    //         {id: "data0", header: ["Interactor", {content: "textFilter"}], css: "rank", width: 120},
    //         {id: "data1", header: ["Interactor", {content: "textFilter"}], width: 120},
    //         {id: "data2", header: "Source", width: 200},
    //         {id: "data3", header: ["Layer", {content: "selectFilter"}], width: 200}
    //     ],
    //     autoheight: true,
    //     autowidth: true,
    //
    //     datatype: "csv",
    //     data: '{{ .Content }}'
    // });
});
