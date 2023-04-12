# data-mining-app

## Objetivos

### Esse aplicativo tem como finalidade apresentar análises realizadas sobre os dados do Tribunal de Contas de Pernambuco pela célula de mineração de dados do Tribunal.

## Desenvolvimento e execução

### Todo o código foi escrito utilizando Python, especificamente a versão 3.8.

### A aplicação é monolítica e para executá-la basta instalar as dependências utilizando o seguinte comando:

    $ make install-dependencies

### Em seguida, basta executar o arquivo ```app.py``` através do seguinte comando no diretório do arquivo:

    $ python3 app.py

### Assim a aplicação será executada na porta 5000 por padrão: ```localhost:5000```


## Deployment

### Para construir a aplicação, utilize o comando:

    $ make build

### Assim, será criado um diretório (current_dir/build) que isola todas as dependências da aplicação. Nesse diretório, um arquivo construído com a base do seu sistema operacional estará disponível para execução.


## Dependências

|  Package   |  Version  |
| :--------: | :-------: |
|   python   |  >= 3.8   |
|    pip3    | >= 21.2.2 |
