# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def index():
    return dict()


def level():
    return dict()

# Página de suporte
def suporte():
    return dict()

# Página de testes

def teste():
    if request.vars.visitor_name:
        session.visitor_name = request.vars.visitor_name
        redirect(URL('suporte'))
    return dict()


# CREATE

def cadastro_fornecedor():
    form = SQLFORM(Fornecedor)
    if form.process().accepted:
        session.flash = 'Novo Fornecedor: %s' % form.vars.nome
        redirect(URL('cadastro_fornecedor'))
    elif form.errors:
        response.flash = 'Erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)

def cadastro_equipamento():
    form = SQLFORM(Equipamento)
    if form.process().accepted:
        session.flash = 'Novo Equipamento: %s' % form.vars.nome
        nome = form.vars.nome
        detalhe = form.vars.descricao
        nome_detalhe = nome + ' ' + detalhe
        db(db.equipamento.id == form.vars.id).update(detalhe=nome_detalhe)
        redirect(URL('cadastro_equipamento'))
    elif form.errors:
        response.flash = 'Erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = ''
    return dict(form=form)

def cadastro_pedido():
    form = SQLFORM(Fornecedor_Equipamento)
    if form.process().accepted:
        session.flash = 'Novo pedido: %s' % form.vars.nome
        redirect(URL('cadastro_pedido'))
    elif form.errors:
        response.flash = 'Erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = ''
    return dict(form=form)

# READ

def ver_fornecedor():
    grid = SQLFORM.grid(Fornecedor, fields =[db.fornecedor.cnpj, db.fornecedor.nome, db.fornecedor.telefone, db.fornecedor.email], maxtextlength=16,exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
    return dict(grid=grid)

def ver_equipamento():
    grid = SQLFORM.grid(Equipamento, fields=[db.equipamento.nome, db.equipamento.descricao] ,maxtextlength=16,exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
    return dict(grid=grid)
