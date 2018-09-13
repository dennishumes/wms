from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import admin
from forms import * 
from .. import db
from ..models import *
from ..funcs_ import *
from sqlalchemy.exc import InvalidRequestError, IntegrityError


def check_admin():
	"""
	Prevent non-admins from accessing the page
	"""
	if not current_user.is_admin:
		abort(403)

def verify_module_access(module):
    """
    check and action that user has access to module

    """
   
    for access in current_user.role.access:
        if access.module.name == module:
            return
        
    abort(403)

def verify_view_access(view):
    """
    check and action that user has access to view
    """
    for access in current_user.role.access:
        if access.views.name == view:
            return

    abort(403)
    
def fetch_sections():
    """
    after module and view check success fetch all sections user has access to
    """
    secs = {}
    for access in current_user.role.access:
        if access.section:
            secs[str(access.section.name)] = access.permission
    return secs

    

# start crud for access
@admin.route('/accesses', methods=['GET', 'POST'])
@login_required
def list_accesses():
    """
    List all accesss
    """
    check_admin()
    verify_module_access('Access')
    verify_view_access('list_accesses')

    user_sections = fetch_sections()
    accesses = Access.query.order_by('module_id')

    return render_template('admin/accesses/accesses.html',
                           accesses=accesses, title="accesses",secs=user_sections)


@admin.route('/accesses/add', methods=['GET', 'POST'])
@login_required
def add_access():
    """
    Add a access to the database
    """
    check_admin()
    verify_module_access('Access')
    verify_view_access('add_access')

    user_sections = fetch_sections()

    add_access = True

    

    form = Dot_(request.form.to_dict());
    
    if form.submit:    
        if form.role and form.module and form.view and form.section and form.permission:
            access_ = Access(role_id=form.role,module_id=form.module,view_id=form.view,section_id=form.section,permission=form.permission)
            try:
            # add access to the database
                db.session.add(access_)
                db.session.commit()

                flash('You have successfully added a new access.')
            except:
                # in case access name already exists
                flash('Error: access name already exists.')

            # redirect to accesss page
            return redirect(url_for('admin.list_accesses'))
        else:
            flash("Error Proccessing Request: Ensure that you select Role-Module-View-Section and then set Permission and if the problem persists contact your systems administrator.")
   
    Roles =  Role.query.order_by('id')
    Modules = Module.query.order_by('id')
   
    # load access template
    return render_template('admin/accesses/access.html', action="Add",
                           add_access=add_access, form=form,
                           title="Add access",Roles=Roles,Modules=Modules,secs=user_sections)


@admin.route('/accesses/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_access(id):
    """
    Edit a role
    """
    check_admin()
    verify_module_access('Access')
    verify_view_access('add_access')

    user_sections = fetch_sections()


    add_access = False

    access = Access.query.get_or_404(id)
    form = Dot_(request.form.to_dict());
   
    if form.submit:    
        if form.role and form.module and form.view and form.section and form.permission:
            access.role_id = form.role
            access.module_id = form.module
            access.view_id = form.view
            access.section_id = form.section
            access.permission = form.permission

            db.session.commit()
            flash('You have successfully edited the access.')

            # redirect to the accesss page
        return redirect(url_for('admin.list_accesses'))


    form.role = access.role_id 
    form.module = access.module_id 
    form.view = access.view_id 
    form.section = access.section_id
    form.permission = access.permission

    Roles =  Role.query.order_by('id')
    Modules = Module.query.order_by('id')

    return render_template('admin/accesses/access.html', action="Edit",
                           add_access=add_access, form=form,
                           access=access, title="Edit access",Roles=Roles,Modules=Modules,secs=user_sections)


@admin.route('/accesses/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_access(id):
    """
    Delete a access from the database
    """
    check_admin()
    verify_module_access('Access')
    
    access = Access.query.get_or_404(id)
    db.session.delete(access)
    db.session.commit()
    flash('You have successfully deleted the access.')

    # redirect to the accesss page
    return redirect(url_for('admin.list_accesses'))

    return render_template(title="Delete access")

# end crud for access



# start crud for modules
@admin.route('/modules', methods=['GET', 'POST'])
@login_required
def list_modules():
    """
    List all modules
    """
    check_admin()
    verify_module_access('Modules')
    verify_view_access('list_modules')

    user_sections = fetch_sections()

    modules = Module.query.all()

    return render_template('admin/modules/modules.html',
                           modules=modules, title="modules",secs=user_sections)


@admin.route('/modules/add', methods=['GET', 'POST'])
@login_required
def add_module():
    """
    Add a module to the database
    """
    check_admin()
    verify_module_access('Modules')
    verify_view_access('add_module')
    user_sections = fetch_sections()


    add_module = True

    form = ModuleForm()
    if form.validate_on_submit():
        module_ = Module(name=form.name.data)
        try:
        # add module to the database
            db.session.add(module_)
            db.session.commit()
 
            flash('You have successfully added a new module.')
        except:
            # in case module name already exists
            flash('Error: Module name already exists.')

        # redirect to modules page
        return redirect(url_for('admin.list_modules'))

    # load module template
    return render_template('admin/modules/module.html', action="Add", add_module=add_module, form=form, title="Add module",secs=user_sections)

@admin.route('/modules/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_module(id):
    """
    Edit a module
    """
    check_admin()
    verify_module_access('Modules')
    verify_view_access('add_module')
    user_sections = fetch_sections()

    add_module = False

    module = Module.query.get_or_404(id)
    form = ModuleForm(obj=module)
    if form.validate_on_submit():
        module.name = form.name.data
     
        db.session.commit()
        flash('You have successfully edited the module.')

        # redirect to the modules page
        return redirect(url_for('admin.list_modules'))

    
    form.name.data = module.name
    return render_template('admin/modules/module.html', action="Edit", add_module=add_module, form=form, module=module, title="Edit Module",secs=user_sections)

@admin.route('/modules/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_module(id):
    """
    Delete a module from the database
    """
    check_admin()
    verify_module_access('Modules')
        
    module = Module.query.get_or_404(id)
    db.session.delete(module)
    db.session.commit()
    flash('You have successfully deleted the module.')

    # redirect to the modules page
    return redirect(url_for('admin.list_modules'))

    return render_template(title="Delete module")


# end crud for modules



# start crud for views
@admin.route('/views', methods=['GET', 'POST'])
@login_required
def module_views():
    """ 
        landing page if user navigates to views page without module id ie.  directly - which is forbidden 
    """
    check_admin()
    return redirect(url_for('home.homepage'))


@admin.route('/views/<module>', methods=['GET', 'POST'])
@login_required
def list_views(module):
    """
    List all views
    """
    check_admin()
    # verify_module_access('Views')
    # verify_view_access('list_views')
    user_sections = fetch_sections()

    views = View.query.all()
    view_all = True
    if module:
        view_all = False
        views = View.query.filter_by(module_id=module)

    module_= Module.query.filter_by(id=module).first()

    return render_template('admin/views/views.html', views=views, title="views",list_all=view_all,module=module_,secs=user_sections)

@admin.route('/views/add', methods=['GET', 'POST'])
@login_required
def add_view_without_module():
    """
        forbidden to route to views without module id
    """
    return redirect(url_for('home.homepage'))



@admin.route('/views/add/<module>', methods=['GET', 'POST'])
@login_required
def add_view(module):
    """
    Add a view to the database
    """
    check_admin()
    # verify_module_access('Views')
    # verify_view_access('add_view')
    user_sections = fetch_sections()

    add_view = True

    form = ViewForm()
    if module == 0:
        form.modules.choices = [(m.id,m.name) for m in Module.query.order_by('id')]
    else:
        form.modules.choices = [(m.id,m.name) for m in Module.query.filter_by(id=module)]

    if form.validate_on_submit():
        view_ = View(name=form.name.data,module_id=form.modules.data)
        try:
        # add view to the database
            db.session.add(view_)
            db.session.commit()
 
            flash('You have successfully added a new view.')
        except:
            # in case view name already exists
            flash('Error: view name already exists.')

        # redirect to views page
        return redirect(url_for('admin.list_views',module=module))

    # load view template
    return render_template('admin/views/view.html', action="Add", add_view=add_view, form=form, title="Add view",module=module,secs=user_sections)

@admin.route('/views/edit', methods=['GET', 'POST'])
@login_required
def view_edit_no_id():
    """
        forbidden to edit view without id
    """
    return redirect(url_for('home.homepage'))

@admin.route('/views/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_view(id):
    """
    Edit a role
    """
    check_admin()
    # verify_module_access('Views')
    # verify_view_access('add_view')
    user_sections = fetch_sections()

    add_view = False

    view = View.query.get_or_404(id)
    form = ViewForm(obj=view)
    form.modules.choices = [(m.id,m.name) for m in Module.query.order_by('id')]

    if form.validate_on_submit():
        view.name = form.name.data
        view.module_id = form.modules.data
        db.session.commit()
        flash('You have successfully edited the view.')

        # redirect to the views page
        return redirect(url_for('admin.list_views',module=view.module_id))

    
    form.name.data = view.name
    form.modules.data = (view.module_id)
    return render_template('admin/views/view.html', action="Edit", add_view=add_view, form=form, view=view, title="Edit view",module=view.module_id,secs=user_sections)

@admin.route('/views/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_view(id):
    """
    Delete a view from the database
    """
    check_admin()
    # verify_module_access('Views')

    view = View.query.get_or_404(id)
    db.session.delete(view)
    db.session.commit()
    flash('You have successfully deleted the view.')

    # redirect to the views page
    return redirect(url_for('admin.list_views',module=module))

    return render_template(title="Delete view")

# end crud for views


# start crud for sections
@admin.route('/sections', methods=['GET', 'POST'])
@login_required
def section_without_view():
    """
        no access to section without view
    """
    return redirect(url_for('home.homepage'))


@admin.route('/sections/<view>', methods=['GET', 'POST'])
@login_required
def list_sections(view):
    """
    List all sections
    """
    check_admin()
    # verify_module_access('Sections')
    # verify_view_access('list_sections')
    user_sections = fetch_sections()
    
    sections = Section.query.all()
    if view:
        sections = Section.query.filter_by(view_id=view)

    view_ = View.query.filter_by(id=view).first()
    return render_template('admin/sections/sections.html', sections=sections, title="sections" ,view=view_,secs=user_sections)


@admin.route('/sections/add')
@login_required
def add_section_no_view():
    """
        cannot reach sections view without view id
    """
    return redirect(url_for('home.homepage'))


@admin.route('/sections/add/<view>', methods=['GET', 'POST'])
@login_required
def add_section(view):
    """
    Add a section to the database
    """
    check_admin()

    # verify_module_access('Sections')
    # verify_view_access('add_section')
    user_sections = fetch_sections()

    add_section = True

    form = SectionForm()
    if view:
        form.views.choices = [(v.id,v.name) for v in View.query.filter_by(id=view)]
    else:
        return redirect(url_for('home.homepage'))
                

    if form.validate_on_submit():
        section_ = Section(name=form.name.data,view_id=form.views.data)
        view_ = View.query.filter_by(id=form.views.data).first()

        try:
        # add section to the database
            db.session.add(section_)
            db.session.commit()
 
            flash('You have successfully added a new section.')
        except InvalidRequestError as e:
            flash('Error: section name already exists.')
            
        except IntegrityError:
            # in case section name already exists
            flash('Error: section name already exists.')

        access_for_role_sysall = Access(role_id=1,module_id=view_.module_id,view_id=form.views.data,section_id=section_.id,permission=3)

        try:
            db.session.add(access_for_role_sysall)
            db.session.commit()
        except InvalidRequestError:
            try:
                flash('Warning: sys.all permissions was not updated automatically.')

            except IntegrityError:
                flash('Warning: sys.all permissions was not updated automatically.')

        # redirect to sections page
        return redirect(url_for('admin.list_sections',view=view))

    # load section template
    return render_template('admin/sections/section.html', action="Add",
                           add_section=add_section, form=form,
                           title="Add section",view=view,secs=user_sections)


@admin.route('/sections/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_section(id):
    """
    Edit a section
    """
    check_admin()
    # verify_module_access('Sections')
    # verify_view_access('add_section')
    user_sections = fetch_sections()

    add_section = False

    section = Section.query.get_or_404(id)
    form = SectionForm(obj=section)

    form.views.choices = [(v.id,v.name) for v in View.query.order_by('id')]

    if form.validate_on_submit():
        section.name = form.name.data
        section.view_id = form.views.data
        db.session.commit()
        flash('You have successfully edited the section.')

        # redirect to the sections page
        return redirect(url_for('admin.list_sections',view=section.view_id))

    
    form.name.data = section.name
    form.views.data = section.view_id
  

    return render_template('admin/sections/section.html', action="Edit",
                           add_section=add_section, form=form,
                           section=section, title="Edit section",view=section.view_id,secs=user_sections)


@admin.route('/sections/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_section(id):
    """
    Delete a section from the database
    """
    check_admin()

    # verify_module_access('Sections')


    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    flash('You have successfully deleted the section.')

    # redirect to the sections page
    return redirect(url_for('admin.list_sections',view=section.view_id))

    return render_template(title="Delete section")

# end crud for sections



# crud operations for user roles
@admin.route('/roles', methods=['GET', 'POST'])
@login_required
def list_roles():
    """
    List all users
    """
    check_admin()
    verify_module_access('Roles')
    verify_view_access('list_roles')
    user_sections = fetch_sections()

    roles = Role.query.all()

    return render_template('admin/roles/roles.html', roles=roles, title="Roles",secs=user_sections)


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()
    verify_module_access('Roles')
    verify_view_access('add_role')
    user_sections = fetch_sections()
    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role_ = Role(name=form.name.data,
                            description=form.description.data)
        try:
        # add role to the database
            db.session.add(role_)
            db.session.commit()
 
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', action="Add",
                           add_role=add_role, form=form,
                           title="Add role",secs=user_sections)


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()
    verify_module_access('Roles')
    verify_view_access('add_role')
    user_sections = fetch_sections()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
       
        # role.password = form.password.data
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', action="Edit", add_role=add_role, form=form, role=role, title="Edit user",secs=user_sections)

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a user from the database
    """
    check_admin()
    verify_module_access('Roles')


    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the users page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete role")




@admin.route('/users', methods=['GET', 'POST'])
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    verify_module_access('Users')
    verify_view_access('list_users')

    user_sections = fetch_sections() 

    return render_template('admin/users/users.html',
                           users=users, title="Users",secs=user_sections)


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Add a user to the database
    """
    check_admin()
    verify_module_access('Users')
    verify_view_access('add_user')
    user_sections = fetch_sections() 
    
    add_user = True

    form = RegistrationForm()
    form.department.choices = [(d.id,d.name) for d in Department.query.order_by('id')]
    form.role.choices = [(r.id,r.name) for r in Role.query.order_by('id')]
    
    if form.validate_on_submit():
        user_ = User(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        try:
        # add user to the database
            db.session.add(user_)
            db.session.commit()
 
            flash('You have successfully added a new user.')
        except:
            # in case user name already exists
            flash('Error: user name already exists.')

        # redirect to users page
        return redirect(url_for('admin.list_users'))

    # load user template

    if 'edit_user_sec' in user_sections:
        if int(user_sections['edit_user_sec']) < 2:
            form.submit.render_kw = {"disabled":"disabled","title":"You require elevated privilege to execute this command."}


    return render_template('admin/users/user.html', action="Add", add_user=add_user, form=form,title="Add user",secs=user_sections)


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Edit a user
    """
    check_admin()
    verify_module_access('Users')
    verify_view_access('add_user')
    user_sections = fetch_sections() 

    add_user = False

    user = User.query.get_or_404(id)
    form = RegistrationForm(obj=user)
    form.department.choices = [(d.id,d.name) for d in Department.query.order_by('id')]
    form.role.choices = [(r.id,r.name) for r in Role.query.order_by('id')]
    form.email.render_kw = {"type":"hidden"}
    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.gender = form.gender.data
        user.contact = form.contact.data
        user.department_id = form.department.data
        user.role_id = form.role.data

        # user.password = form.password.data
        db.session.commit()
        flash('You have successfully edited the user.')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))

    form.username.data = user.username
    form.email.data = user.email
   

    return render_template('admin/users/user.html', action="Edit", add_user=add_user, form=form, user=user, title="Edit user",secs=user_sections)

@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a user from the database
    """
    check_admin()
    verify_module_access('Users')

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the users page
    return redirect(url_for('admin.list_users'))

    return render_template(title="Delete user")
# end users crud

# start department crud
@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()
    verify_module_access('Departments')
    verify_view_access('list_departments')
    user_sections = fetch_sections() 

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments",secs=user_sections)


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    verify_module_access('Departments')
    verify_view_access('add_department')
    user_sections = fetch_sections() 

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department",secs=user_sections)


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()
    verify_module_access('Departments')
    verify_view_access('add_department')
    user_sections = fetch_sections() 


    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department",secs=user_sections)


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    verify_module_access('Departments')

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")
# end department crud

# start warehouse crud
@admin.route('/warehouses', methods=['GET', 'POST'])
@login_required
def list_warehouses():
    """
    List all warehouses
    """
    check_admin()
    verify_module_access('Warehouses')
    verify_view_access('list_warehouses')

    user_sections = fetch_sections() 

    warehouses = Warehouse.query.all()

    return render_template('admin/warehouses/warehouses.html',
                           warehouses=warehouses, title="warehouses",secs=user_sections)


@admin.route('/warehouses/add', methods=['GET', 'POST'])
@login_required
def add_warehouse():
    """
    Add a warehouse to the database
    """
    check_admin()

    verify_module_access('Warehouses')
    verify_view_access('add_warehouse')
    user_sections = fetch_sections() 

    add_warehouse = True

    form = WarehouseForm()
    form.locations.choices = [(l.id,l.name) for l in Location.query.order_by('id')]

    if form.validate_on_submit():
        warehouse = Warehouse(name=form.name.data,
                                description=form.description.data,location_id=form.locations.data)
        try:
            # add warehouse to the database
            db.session.add(warehouse)
            db.session.commit()
            flash('You have successfully added a new warehouse.')
        except:
            # in case warehouse name already exists
            flash('Error: warehouse name already exists.')

        # redirect to warehouses page
        return redirect(url_for('admin.list_warehouses'))

    # load warehouse template
    return render_template('admin/warehouses/warehouse.html', action="Add",
                           add_warehouse=add_warehouse, form=form,
                           title="Add warehouse",secs=user_sections)


@admin.route('/warehouses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_warehouse(id):
    """
    Edit a warehouse
    """
    check_admin()
    verify_module_access('Warehouses')
    verify_view_access('add_warehouse')

    user_sections = fetch_sections() 


    add_warehouse = False

    warehouse = Warehouse.query.get_or_404(id)
    form = WarehouseForm(obj=warehouse)
    form.locations.choices = [(l.id,l.name) for l in Location.query.order_by('id')]

    if form.validate_on_submit():
        warehouse.name = form.name.data
        warehouse.description = form.description.data
        warehouse.location_id = form.locations.data
        db.session.commit()
        flash('You have successfully edited the warehouse.')

        # redirect to the warehouses page
        return redirect(url_for('admin.list_warehouses'))

    form.description.data = warehouse.description
    form.name.data = warehouse.name
    form.locations.data = warehouse.location_id
    return render_template('admin/warehouses/warehouse.html', action="Edit",
                           add_warehouse=add_warehouse, form=form,
                           warehouse=warehouse, title="Edit warehouse",secs=user_sections)


@admin.route('/warehouses/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_warehouse(id):
    """
    Delete a warehouse from the database
    """
    check_admin()

    verify_module_access('Warehouses')

    warehouse = Warehouse.query.get_or_404(id)
    db.session.delete(warehouse)
    db.session.commit()
    flash('You have successfully deleted the warehouse.')

    # redirect to the warehouses page
    return redirect(url_for('admin.list_warehouses'))

    return render_template(title="Delete warehouse")

# end warehouse crud

# start location crud
@admin.route('/locations', methods=['GET', 'POST'])
@login_required
def list_locations():
    """
    List all locations
    """
    check_admin()
    verify_module_access('Locations')
    verify_view_access('list_locations')
    user_sections = fetch_sections() 

    locations = Location.query.all()

    return render_template('admin/locations/locations.html',
                           locations=locations, title="locations",secs=user_sections)


@admin.route('/locations/add', methods=['GET', 'POST'])
@login_required
def add_location():
    """
    Add a location to the database
    """
    check_admin()

    verify_module_access('Locations')
    verify_view_access('add_location')
    user_sections = fetch_sections() 

    add_location = True

    form = LocationForm()
    if form.validate_on_submit():
        location = Location(name=form.name.data,
                                description=form.address.data)
        try:
            # add location to the database
            db.session.add(location)
            db.session.commit()
            flash('You have successfully added a new location.')
        except:
            # in case location name already exists
            flash('Error: location name already exists.')

        # redirect to locations page
        return redirect(url_for('admin.list_locations'))

    # load location template
    return render_template('admin/locations/location.html', action="Add",
                           add_location=add_location, form=form,
                           title="Add location",secs=user_sections)


@admin.route('/locations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_location(id):
    """
    Edit a location
    """
    check_admin()
    verify_module_access('Locations')
    verify_view_access('add_location')
    user_sections = fetch_sections() 


    add_location = False

    location = Location.query.get_or_404(id)
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        location.name = form.name.data
        location.address = form.address.data
        db.session.commit()
        flash('You have successfully edited the location.')

        # redirect to the locations page
        return redirect(url_for('admin.list_locations'))

    form.address.data = location.address
    form.name.data = location.name
    return render_template('admin/locations/location.html', action="Edit",
                           add_location=add_location, form=form,
                           location=location, title="Edit location",secs=user_sections)


@admin.route('/locations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_location(id):
    """
    Delete a location from the database
    """
    check_admin()

    verify_module_access('Locations')

    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    flash('You have successfully deleted the location.')

    # redirect to the locations page
    return redirect(url_for('admin.list_locations'))

    return render_template(title="Delete location")
# end location crud

# start bin crud
@admin.route('/bins',methods=['GET', 'POST'])
@login_required
def list_bin_without_warehouse():
    """ 
        landing page if user navigates to bins page without warehouse id ie.  directly - which is forbidden 
    """
    check_admin()
    return redirect(url_for('home.homepage'))


@admin.route('/bins/<warehouse>', methods=['GET', 'POST'])
@login_required
def list_bins(warehouse):
    """
    List all bins
    """
    check_admin()
    verify_module_access('Bins')
    verify_view_access('list_bins')
    user_sections = fetch_sections() 

    bins = Bin.query.filter_by(warehouse_id=warehouse)

    return render_template('admin/bins/bins.html',
                           bins=bins, title="bins",secs=user_sections,warehouse=warehouse)

@admin.route('/bins/add',methods=['GET', 'POST'])
@login_required
def add_bin_without_warehouse():
    """ 
        landing page if user navigates to bin add page without warehouse id ie.  directly - which is forbidden 
    """
    check_admin()
    return redirect(url_for('home.homepage'))


@admin.route('/bins/add/<warehouse>', methods=['GET', 'POST'])
@login_required
def add_bin(warehouse):
    """
    Add a bin to the database
    """
    check_admin()

    verify_module_access('Bins')
    verify_view_access('add_bin')
    user_sections = fetch_sections() 

    add_bin = True
    error = 0
    form = BinForm()
    form.depth.data = 1
    
    if form.validate_on_submit():
        
        if int(form.multi.data) == 1:
            error = addMultiBins(form,warehouse)
            if not error:
                flash('Bins added successfully.')
            else:
                flash('Error: %s.'%error)

        else:
            bin_ = Bin(name=form.name.data,warehouse_id=warehouse,depth=form.depth.data)
            try:
            # add bin to the database
                db.session.add(bin_)
                db.session.commit()
                flash('You have successfully added a new bin.')
            except:
            # in case bin name already exists
                flash('Error: bin name already exists.')

        

        
        # redirect to bins page if not error
        if not error:
            return redirect(url_for('admin.list_bins', warehouse=warehouse))

    # load bin template
    return render_template('admin/bins/bin.html', action="Add",
                           add_bin=add_bin, form=form,
                           title="Add Bin",secs=user_sections,warehouse=warehouse)


@admin.route('/bins/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bin(id):
    """
    Edit a bin
    """
    check_admin()
    verify_module_access('Bins')
    verify_view_access('add_bin')
    user_sections = fetch_sections() 


    add_bin = False

    bin_ = Bin.query.get_or_404(id)
    form = BinForm(obj=bin_)
    if form.validate_on_submit():
        bin_.name = form.name.data
        bin_.warehouse_id = form.warehouse.data
        db.session.commit()
        flash('You have successfully edited the bin.')

        # redirect to the bins page
        return redirect(url_for('admin.list_bins'))

    form.warehouse.data = bin_.warehouse_id
    form.name.data = bin_.name
    return render_template('admin/bins/bin.html', action="Edit",
                           add_bin=add_bin, form=form,
                           bin=bin_, title="Edit Bin",secs=user_sections,warehouse=warehouse)


@admin.route('/bins/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_bin(id):
    """
    Delete a bin from the database
    """
    check_admin()

    verify_module_access('Bins')

    bin_ = Bin.query.get_or_404(id)
    db.session.delete(bin_)
    db.session.commit()
    flash('You have successfully deleted the bin.')

    # redirect to the bins page
    return redirect(url_for('admin.list_bins',warehouse=bin_.warehouse_id))

    return render_template(title="Delete Bin")
# end location crud
