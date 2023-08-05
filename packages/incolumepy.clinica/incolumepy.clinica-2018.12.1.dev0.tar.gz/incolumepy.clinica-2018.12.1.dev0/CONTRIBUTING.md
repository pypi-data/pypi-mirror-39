# Guia de contribuição
## Repositório de desenvolvimento Local
Configure o repositório de desenvolvimento local conforme o tutorial: https://brito.blog.incolume.com.br/2018/11/repositorio-pypi-local-com-devpi-server.html.

### Ativar o servidor pypi local
```devpi-server --stop && devpi-server --start && devpi use http://localhost:3141/root/```

## Regras para codigicação
1. Criar um novo **branch** para cada etapa de codificação.
1. Crie o branch sempre a partir do master
1. As **branches** terão finalidades específicas:
    * Introduzir novas funcionalidades (**feature**)
    * Corrigir comportamento inesperado (**bug**)
    * Corrigir comportamento inesperado que compromete o funcionamento (**critical**)
    * Alterar a forma, mantendo o comportamento (**refactor**)
1. O nome da **branch deve ser prefixado com o tipo de alteração que será realizada** : (feature, bug, critical ou refactor)
   * exemplos via terminal:
      - bug/issue#21:
      ```git co -b bug/issue#21 origin/master```
      - critical/issue#13:
      ```git co -b critical/issue#13 origin/master```
      - feature/issue#23:
      ```git co -b feature/issue#23 origin/master```
      - refactor/issue#30:
      ```git co -b refactor/issue#30 origin/master```
   * Detalhes sobre git via terminal:
     - [Guia Rápido de comandos git (lado usuário)](http://brito.blog.incolume.com.br/2013/03/guia-rapido-de-comandos-git-lado-usuario.html)

## Outros Detalhes
- [wiki do projeto](https://gitlab.com/clinicaesteticabrito/inventario_clinica/wikis/home)
