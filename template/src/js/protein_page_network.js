function onCytoscapeElementClicked(event) {
    var currentTime = new Date().getTime();
    if(currentTime - lastClickTimeMs < 500) {
      console.log("cytoscape double-click event:" + event.cyTarget.id())
      ("{{ .Site.BaseURL }}/protein/"+event.cyTarget.id());
    }
    lastClickTimeMs = currentTime;
}

var lastClickTimeMs = 0

$(document).ready(function(){
    var cy = cytoscape({
        container: $('#interactionnetworkdiv'),
        elements: JSON.parse(document.getElementById('interactionnetworkdata').value),
        userZoomingEnabled: false,
        layout: {
            name: 'cose-bilkent'
        },
        style: [
            {
                selector: 'node[main]',
                style: {
                    'height': 30,
                    'width': function( ele ){ return ele.data('id').length*10+20 },
                    'shape': 'roundrectangle',
                    'background-color': '#216869',
                    'label': 'data(id)',
                    'text-halign': 'center',
                    'text-valign': 'center'
                }
            },
            {
                selector: 'node[!main]',
                style: {
                    'height': 30,
                    'width': function( ele ){ return ele.data('id').length*10+20 },
                    'shape': 'roundrectangle',
                    'background-color': '#9cc5a1',
                    'label': 'data(id)',
                    'text-halign': 'center',
                    'text-valign': 'center'
                }
            },
            {
                selector: 'edge',
                style: {
                  'width': 3,
                  'curve-style': 'bezier',
                  'line-color': '#000',
                  'target-arrow-color': '#000',
                  'target-arrow-shape': 'none'
                }
            },
            {
                selector: 'edge[type="Transcriptional_regulatory"]',
                style: {
                  'line-color': '#A7A37E',
                  'target-arrow-color': '#A7A37E',
                  'target-arrow-shape': 'triangle'
                }
            },
            {
                selector: 'edge[type="Metabolic"]',
                style: {
                  'line-color': '#046380',
                  'target-arrow-color': '#046380',
                  'target-arrow-shape': 'none'
                }
            },
            {
                selector: 'edge[type="PPI"]',
                style: {
                  'line-color': '#002F2F',
                  'target-arrow-color': '#002F2F',
                  'target-arrow-shape': 'none'
                }
            }
        ]
    });
    cy.fit();
    interactionnetworkcontrolldiv = webix.ui({
        container:"interactionnetworkcontrolldiv",
        view: "form",
        borderless:true,
        paddingY: 5,
        paddingX: 10,
        cols:[
            {view: "button", label: "Download image", width: 200, click:function(){webix.html.download(cy.png(), "SalmoNet_"+document.getElementById('uniprot').innerHTML+".png")}},
            {view: "button", type:"iconButton", icon: "arrows-alt", align:"right", width: 35, click:function(){cy.fit()}},
            {view: "button", type:"iconButton", icon: "plus", width: 35, align:"right", click:function(){cy.zoom(cy.zoom()+0.5)}},
            {view: "button", type:"iconButton", icon: "minus", width: 35, align:"right", click:function(){cy.zoom(cy.zoom()-0.5)}},
        ]
    });
    cy.elements('edge').qtip({
        content: function(){
            return this.data("type") +
                ' interaction between ' +
                this.source().data("id") +
                ' and ' +
                this.target().data("id")
        },
        position: {
            my: 'top center',
            at: 'bottom center'
        },
        style: {
            classes: 'qtip-bootstrap',
            tip: {
                width: 16,
                height: 8
            }
        },
        show: {
            event: 'mouseover'
        },
        hide: {
            event: 'mouseout'
        },
    });
    interactionnetworkcontrolldiv.define("width", $("#interactionnetworkcontrolldiv").width());
    interactionnetworkcontrolldiv.resize();
    cy.on('tap', 'node[!main]', onCytoscapeElementClicked);
});
$(window).resize(function() {
    interactionnetworkcontrolldiv.define("width", $("#interactionnetworkcontrolldiv").width());
    interactionnetworkcontrolldiv.resize();
});
