String.prototype.titleCase = function() {
  return this.replace(/\w\S*/g, function(txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
};

String.prototype.twoReplace = function(r1, r2) {
  return this.replace(r1, r2).replace(r1, r2)
}

String.prototype.replaceTitle = function() {
  return this.twoReplace("_", " ").titleCase()
}

var get_endpoint = function(url) {
  var archivo = null;
  $.ajax({
    'async': false,
    'global': false,
    'url': url,
    'dataType': "json",
    'success': function(data) {
      archivo = data;
    }
  });
  return archivo;
};

var remove_elem = function(elem) {
  for (var i = 0; i < elem.length; i++) {
    $(elem[i]).remove()
  }
}

var graficos = get_endpoint('/graficos')
var corredores = graficos['graficos']['corredores']
var periodos = graficos['graficos']['periodos']

var each_array = function(array, id) {
  $.each(array, function(i, elem) {
    if (id == 'periodos') elem = elem.replace("_", " ")
    if (id == 'list_corredores') elem = elem.replaceTitle()
    $('#' + id).append($('<option>', {
      value: elem,
      text: elem,
      id: elem
    }));
  });
}

each_array(periodos, 'periodos')
each_array(corredores, 'list_corredores')

var insert_graficos = function(id) {
  console.log("id", id)

  remove_elem(['h2', 'embed'])

  var graphs = {
    'graficos': []
  }

  select_periodo = $("#periodos option:selected").attr('id').replace(" ", "_")
  select_filtros = $("#filtros option:selected").attr('id')

  if (id == "generales") {
    $("#list_corredores").hide()
    graphs = get_endpoint('/generales' + "/" + select_periodo)
  } else if (id == 'corredores') {
    select_corredor = $("#list_corredores option:selected").attr('id').twoReplace(" ", "_").toLowerCase()
    $("#list_corredores").show()
    graphs = get_endpoint('/corredores' + "/" + select_periodo + "/" + select_corredor)
  } else if (id == 'periodos') {
    if (select_filtros == 'generales') {
      graphs = get_endpoint('/generales' + "/" + select_periodo)
    } else {
      select_corredor = $("#list_corredores option:selected").attr('id').twoReplace(" ", "_").toLowerCase()
      graphs = get_endpoint('/corredores' + "/" + select_periodo + "/" + select_corredor)
    }
  }


  $.each(graphs['graficos'], function(i, grafico) {
    $('#entry').append(
      $('<h2>', {
        text: grafico.title,
        style: "color:white"
      }),
      $('<embed>', {
        value: grafico.name,
        text: grafico.title,
        src: grafico.filename
      })
    )
  });

}

$('body').on('change', '#filtros', function() {
  $("#filtros option:selected").attr('id', function(a, id_selc, c) {
    console.log("selecciono el periodo filtros")
    insert_graficos(id_selc)
    if (id_selc == 'corredores') {
      $("#select_corredores")
    }
  })
});

$('body').on('change', '#list_corredores', function() {
  $("#list_corredores option:selected").attr('id', function(a, id_selc, c) {
    console.log("selecciono el periodo list_corredores")
    insert_graficos("corredores")
  })
});

$('body').on('change', '#periodos', function() {
  $("#periodos option:selected").attr('id', function(a, id_selc, c) {
    console.log("selecciono el periodo periodos")
    insert_graficos("periodos")
  })
});

$(document).ready(function() {
  insert_graficos("generales")
  $("#salir").click(function() {
    window.location = "/logout";
  });

  //Vuelvo al home cuando clickeo el logo
  $("#logo").click(function() {
    window.location = "/";
  });
});