
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>João Transações</title>
  <link rel="stylesheet" href="static/styles.css">
  <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
      crossorigin="anonymous"></script>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lilita+One&display=swap" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Black+Ops+One&display=swap" rel="stylesheet">
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
  <link rel="shortcut icon" href="/static/favicon_io/favicon.ico" type="image/x-icon">
  <style>
    .bg-black-dark{
    background-color: #121212;
    color: white;
}
    a:hover{
    color: white;
    text-decoration: none;
}
          body {
          background-color: #110070;
          color: #fff;
          font-family: 'Arial', sans-serif;
      }

      a {
          color: white;
          text-decoration: none;
      }

.link_nav_active{
  background-color: #00ff91;
}
    /* Estilo para a barra lateral */
    .sidebar {
      position: fixed;
      top: 0;
      bottom: 0;
      left: 0;
      z-index: 100;
      padding: 48px 0 0;
      margin-top: auto;
      box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
    }

    /* Estilo para o conteúdo principal */
    .content {
      margin-left: 250px;
      padding: 20px;
    }

    /* Estilos específicos para dispositivos móveis */
    @media (max-width: 768px) {
      .sidebar {
        width: 100%;
        position: relative;
        padding-top: 56px; /* Ajuste conforme necessário */
      }
      .content {
        margin-left: 0;
        padding: 10px;
      }
      /* Outros ajustes de estilo */
    }
  </style>

<!-- SCRIPTS -->
<script>
    function openModal() {
        document.getElementById('addTransactionModal').style.display = 'flex';
    }

    function closeModal() {
        document.getElementById('addTransactionModal').style.display = 'none';
    }

    function openFilterModal() {
        document.getElementById('filterModal').style.display = 'flex';
    }

    function closeFilterModal() {
        document.getElementById('filterModal').style.display = 'none';
    }


    
    // Close modais ao clicar fora da área do modal
    window.onclick = function (event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };

// Adiciona classes condicionais com base no valor do saldo
var saldo = parseFloat(document.getElementById('saldo').innerText);
var saldoCard = document.getElementById('saldoCard');
var receitasCard = document.getElementById('receitasCard');
var despesasCard = document.getElementById('despesasCard');

if (saldo > 0) {
    saldoCard.classList.add('positive');
    receitasCard.style.fill = '#00ffbf';  // Altera a cor para verde
    despesasCard.style.fill = '#ff0044';   // Altera a cor para vermelho
} else if (saldo < 0) {
    saldoCard.classList.add('negative');
    receitasCard.style.fill = '#00ffbf';  // Altera a cor para verde
    despesasCard.style.fill = '#ff0044';   // Altera a cor para vermelho
} else {
    saldoCard.classList.add('zero');
    receitasCard.style.fill = '#8c00ff';  // Mantém a cor roxa
    despesasCard.style.fill = '#8c00ff';  // Mantém a cor roxa
}

</script>
</head>
<body>
<!-- Adicione este conteúdo dentro do seu formulário principal -->

  <div class="container-fluid">
    <div class="row">


      <!-- Barra lateral -->
      <nav class="col-md-3 col-lg-2 d-md-block  sidebar">
        <div class="logo_nav">
            <img src="/static/logo.png" style="height:150px" alt="">
        </div>
        <div class="sidebar-sticky">
          <ul class="nav flex-column">
            <div class="d-flex links_nav icon_active">
                <a href="{{ url_for('index') }}"  title="DashBoard">
                    <i class='bx bxs-objects-horizontal-left icon-side'></i>
                    <span>DashBoard</span>
                </a>
            </div>
    
            <div class="d-flex links_nav ">
                <a href="{{ url_for('tabela') }}" title="Transações">
    
                    <i class='bx bxs-bank icon-side'></i>
                    <span>Transações</span>
    
                </a>
            </div>
    
            <div class="d-flex links_nav">
                <a href="/pessoas_empresas" title="Pessoas Ou Empresas">
                    <i class='bx bx-user-pin icon-side'></i>
                    <span>Pessoas</span>
    
                </a>
            </div>
            <div class="d-flex links_nav">
                <a href="/templates" title="Relatorios">
                    <i class='bx bx-file-find icon-side '></i>
                    <span>Templates</span>
                </a>
            </div>
          </ul>
        </div>
      </nav>

      <!-- Conteúdo principal -->
      <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-md-4 content">
  
          
        <div class=" header">DashBoard</div>
        <br>
        <div class='row dashboard-cards text-dark' href="" style="color: black;">
            <div class='card col-md-4'>
              <div class='card-title'>
                <h1 style="color: black;">
                    Receitas <span class="ml-1">
                        <svg xmlns="http://www.w3.org/2000/svg" style="height: 30px;box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px;" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#00d9bf" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM135.1 217.4l107.1-99.9c3.8-3.5 8.7-5.5 13.8-5.5s10.1 2 13.8 5.5l107.1 99.9c4.5 4.2 7.1 10.1 7.1 16.3c0 12.3-10 22.3-22.3 22.3H304v96c0 17.7-14.3 32-32 32H240c-17.7 0-32-14.3-32-32V256H150.3C138 256 128 246 128 233.7c0-6.2 2.6-12.1 7.1-16.3z"/></svg>
                      </span>
                </h1>
                <span class="value">
                 <h4 style="color:#00d9bf ;"> <span class="text-dark">R$</span> {{ total_receitas }}</h4>
               </span>
              </div>
            </div>
            <div class='card col-md-4'>
                <div class='card-title'>
                  <h1 style="color: black;">
                      Depesas <span class="ml-1">
                        <svg xmlns="http://www.w3.org/2000/svg"  style="height: 30px;box-shadow: rgba(7, 255, 197, 0.2) 0px 7px 29px 0px;"viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#ff0000"  d="M256 0a256 256 0 1 0 0 512A256 256 0 1 0 256 0zM376.9 294.6L269.8 394.5c-3.8 3.5-8.7 5.5-13.8 5.5s-10.1-2-13.8-5.5L135.1 294.6c-4.5-4.2-7.1-10.1-7.1-16.3c0-12.3 10-22.3 22.3-22.3l57.7 0 0-96c0-17.7 14.3-32 32-32l32 0c17.7 0 32 14.3 32 32l0 96 57.7 0c12.3 0 22.3 10 22.3 22.3c0 6.2-2.6 12.1-7.1 16.3z"/></svg> 
                      </span>
                  </h1>
                  <span class="value">
                       <h4 style="color:#ff0000 ;"> <span class="text-dark">R$</span> {{ total_despesas }}</h4>
                  </span>
                </div>
              </div>
              <div class='card col-md-4'>
                <div class='card-title'>
                  <h1 style="color: black;">
                      Total <span class="ml-1">
                        <svg xmlns="http://www.w3.org/2000/svg" style="height: 30px;" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#4c00ff" d="M156.6 384.9L125.7 354c-8.5-8.5-11.5-20.8-7.7-32.2c3-8.9 7-20.5 11.8-33.8L24 288c-8.6 0-16.6-4.6-20.9-12.1s-4.2-16.7 .2-24.1l52.5-88.5c13-21.9 36.5-35.3 61.9-35.3l82.3 0c2.4-4 4.8-7.7 7.2-11.3C289.1-4.1 411.1-8.1 483.9 5.3c11.6 2.1 20.6 11.2 22.8 22.8c13.4 72.9 9.3 194.8-111.4 276.7c-3.5 2.4-7.3 4.8-11.3 7.2v82.3c0 25.4-13.4 49-35.3 61.9l-88.5 52.5c-7.4 4.4-16.6 4.5-24.1 .2s-12.1-12.2-12.1-20.9V380.8c-14.1 4.9-26.4 8.9-35.7 11.9c-11.2 3.6-23.4 .5-31.8-7.8zM384 168a40 40 0 1 0 0-80 40 40 0 1 0 0 80z"/></svg>
                      </span>
                  </h1>
                  <span class="value">
                    <h4 style="color:#4c00ff ;"> <span class="text-dark">R$</span> {{ total }}</h4>
               </span>
                </div>
              </div>

          </div>
          <!-- Graficos -->
          <div class='row dashboard-cards text-dark' href="" style="color: black;">

          <div class='card col-md-7' style='width: 550px;'>
            <div class='card-title'>
                <h4 style="color: black;">
                Comparação Mensal
                </h4>
                <span class="value">
                    <canvas id="areaChart" width="400" height="200"></canvas>
                    
                </span>
            </div>
        </div>
        <div class='card col-md-7' style='width: 350px;margin-left: auto;'>
            <div class='card-title'>
                <h4 style="color: black;">
                Comparação De pagamento
                </h4>
                <span class="value">
                    <canvas id="pieChart" width="200" height="100"></canvas>
                </span>
            </div>
        </div>

           
            </div>

          </div>

        </div>
      </main>
    </div>
  </div>







<script>
    $(document).ready(function(){
  var zindex = 10;
  
  $("div.card").click(function(e){
    e.preventDefault();

    var isShowing = false;

    if ($(this).hasClass("d-card-show")) {
      isShowing = true
    }

    if ($("div.dashboard-cards").hasClass("showing")) {
      // a card is already in view
      $("div.card.d-card-show")
        .removeClass("d-card-show");

      if (isShowing) {
        // this card was showing - reset the grid
        $("div.dashboard-cards")
          .removeClass("showing");
      } else {
        // this card isn't showing - get in with it
        $(this)
          .css({zIndex: zindex})
          .addClass("d-card-show");

      }

      zindex++;

    } else {
      // no dashboard-cards in view
      $("div.dashboard-cards")
        .addClass("showing");
      $(this)
        .css({zIndex:zindex})
        .addClass("d-card-show");

      zindex++;
    }
    
  });
});
</script>
<script>

        var formaPagamentoData = {{ forma_pagamento_data | tojson }};

        var totalReceitas = {{ total_receitas  }};
        var totalDespesas = {{ total_despesas  }};

        document.addEventListener('DOMContentLoaded', function() {
    var areaCtx = document.getElementById('areaChart').getContext('2d');
    var areaChart = new Chart(areaCtx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Despesas',
                    data: totalDespesas,
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Receitas',
                    data: totalReceitas,
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});

console.log(totalReceitas);
console.log(totalDespesas);



        // Gráfico de Pizza
        var pieCtx = document.getElementById('pieChart').getContext('2d');
        var pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(formaPagamentoData),
                datasets: [{
                    data: Object.values(formaPagamentoData),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            }
        });
</script>

  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
