import logging

import jwt

from .. import entities, miscellaneous, exceptions, services

logger = logging.getLogger(name='dtlpy')


class Projects:
    """
    Projects repository
    """

    def __init__(self, client_api: services.ApiClient, org=None):
        self._client_api = client_api
        self._org = org

    def __get_from_cache(self) -> entities.Project:
        project = self._client_api.state_io.get('project')
        if project is not None:
            project = entities.Project.from_json(_json=project, client_api=self._client_api)
        return project

    def __get_by_id(self, project_id: str) -> entities.Project:
        """
        :param project_id:
        """
        success, response = self._client_api.gen_request(req_type='get',
                                                         path='/projects/{}'.format(project_id))
        if success:
            project = entities.Project.from_json(client_api=self._client_api,
                                                 _json=response.json())
        else:
            # raise PlatformException(response)
            # TODO because of a bug in gate wrong error is returned so for now manually raise not found
            raise exceptions.PlatformException(error="404", message="Project not found")
        return project

    def __get_by_identifier(self, identifier=None) -> entities.Project:
        """
        :param identifier:
        """
        projects = self.list()
        projects_by_name = [project for project in projects if identifier in project.id or identifier in project.name]
        if len(projects_by_name) == 1:
            return projects_by_name[0]
        elif len(projects_by_name) > 1:
            raise Exception('Multiple projects with this name/identifier exist')
        else:
            raise Exception("Project not found")

    @property
    def platform_url(self):
        return self._client_api._get_resource_url("projects")

    def open_in_web(self, project_name: str = None, project_id: str = None, project: entities.Project = None):
        """
        :param project_name:
        :param project_id:
        :param project:
        """
        if project_name is not None:
            project = self.get(project_name=project_name)
        if project is not None:
            project.open_in_web()
        elif project_id is not None:
            self._client_api._open_in_web(url=self.platform_url + '/' + str(project_id))
        else:
            self._client_api._open_in_web(url=self.platform_url)

    def checkout(self,
                 identifier: str = None,
                 project_name: str = None,
                 project_id: str = None,
                 project: entities.Project = None):
        """
        Check-out a project
        :param identifier: project name or partial id
        :param project_name:
        :param project_id:
        :param project:
        :return:
        """
        if project is None:
            if project_id is not None or project_name is not None:
                project = self.get(project_id=project_id, project_name=project_name)
            elif identifier is not None:
                project = self.__get_by_identifier(identifier=identifier)
            else:
                raise exceptions.PlatformException(error='400',
                                                   message='Must provide partial/full id/name to checkout')
        self._client_api.state_io.put('project', project.to_json())
        logger.info('Checked out to project {}'.format(project.name))

    def _send_mail(self, project_id: str, send_to: str, title: str, content: str) -> bool:
        if project_id:
            url = '/projects/{}/mail'.format(project_id)
        else:
            url = '/outbox'
        assert isinstance(title, str)
        assert isinstance(content, str)
        if self._client_api.token is not None:
            sender = jwt.decode(self._client_api.token, algorithms=['HS256'],
                                verify=False, options={'verify_signature': False})['email']
        else:
            raise exceptions.PlatformException('600', 'Token expired please log in')

        payload = {
            'to': send_to,
            'from': sender,
            'subject': title,
            'body': content
        }

        success, response = self._client_api.gen_request(req_type='post',
                                                         path=url,
                                                         json_req=payload)

        if not success:
            raise exceptions.PlatformException(response)
        return True

    def add_member(self, email: str, project_id: str, role: entities.MemberRole = entities.MemberRole.DEVELOPER):
        """
        :param email:
        :param project_id:
        :param role: "owner" ,"engineer" ,"annotator" ,"annotationManager"
        """
        url_path = '/projects/{}/members/{}'.format(project_id, email)
        payload = dict(role=role)

        if role not in list(entities.MemberRole):
            raise ValueError('Unknown role {!r}, role must be one of: {}'.format(role,
                                                                                 ', '.join(list(entities.MemberRole))))

        success, response = self._client_api.gen_request(req_type='post',
                                                         path=url_path,
                                                         json_req=payload)
        if not success:
            raise exceptions.PlatformException(response)

        return response.json()

    def update_member(self, email: str, project_id: str, role: entities.MemberRole = entities.MemberRole.DEVELOPER):
        """
        :param email:
        :param project_id:
        :param role: "owner" ,"engineer" ,"annotator" ,"annotationManager"
        """
        url_path = '/projects/{}/members/{}'.format(project_id, email)
        payload = dict(role=role)

        if role not in list(entities.MemberRole):
            raise ValueError('Unknown role {!r}, role must be one of: {}'.format(role,
                                                                                 ', '.join(list(entities.MemberRole))))

        success, response = self._client_api.gen_request(req_type='patch',
                                                         path=url_path,
                                                         json_req=payload)
        if not success:
            raise exceptions.PlatformException(response)

        return response.json()

    def remove_member(self, email: str, project_id: str):
        """
        :param email:
        :param project_id:
        """
        url_path = '/projects/{}/members/{}'.format(project_id, email)
        success, response = self._client_api.gen_request(req_type='delete',
                                                         path=url_path)
        if not success:
            raise exceptions.PlatformException(response)

        return response.json()

    def list_members(self, project: entities.Project, role: entities.MemberRole = None):
        """
        :param project:
        :param role: "owner" ,"engineer" ,"annotator" ,"annotationManager"
        """
        url_path = '/projects/{}/members'.format(project.id)

        if role is not None and role not in list(entities.MemberRole):
            raise ValueError('Unknown role {!r}, role must be one of: {}'.format(role,
                                                                                 ', '.join(list(entities.MemberRole))))

        success, response = self._client_api.gen_request(req_type='get',
                                                         path=url_path)
        if not success:
            raise exceptions.PlatformException(response)

        members = miscellaneous.List(
            [entities.User.from_json(_json=user, client_api=self._client_api, project=project) for user in
             response.json()])

        if role is not None:
            members = [member for member in members if member.role == role]

        return members

    def list(self) -> miscellaneous.List[entities.Project]:
        """
        Get users project's list.
        :return: List of Project objects
        """
        if self._org is None:
            url_path = '/projects'
        else:
            url_path = '/orgs/{}/projects'.format(self._org.id)
        success, response = self._client_api.gen_request(req_type='get',
                                                         path=url_path)

        if success:
            pool = self._client_api.thread_pools(pool_name='entity.create')
            projects_json = response.json()
            jobs = [None for _ in range(len(projects_json))]
            # return triggers list
            for i_project, project in enumerate(projects_json):
                jobs[i_project] = pool.submit(entities.Project._protected_from_json,
                                              **{'client_api': self._client_api,
                                                 '_json': project})

            # get all results
            results = [j.result() for j in jobs]
            # log errors
            _ = [logger.warning(r[1]) for r in results if r[0] is False]
            # return good jobs
            projects = miscellaneous.List([r[1] for r in results if r[0] is True])
        else:
            logger.error('Platform error getting projects')
            raise exceptions.PlatformException(response)
        return projects

    def get(self,
            project_name: str = None,
            project_id: str = None,
            checkout: bool = False,
            fetch: bool = None) -> entities.Project:
        """
        Get a Project object
        :param project_name: optional - search by name
        :param project_id: optional - search by id
        :param checkout:
        :param fetch: optional - fetch entity from platform, default taken from cookie
        :return: Project object

        """
        if fetch is None:
            fetch = self._client_api.fetch_entities

        if project_id is None and project_name is None:
            project = self.__get_from_cache()
            if project is None:
                raise exceptions.PlatformException(
                    error='400',
                    message='No checked-out Project was found, must checkout or provide an identifier in inputs')
        elif fetch:
            if project_id is not None:
                if not isinstance(project_id, str):
                    raise exceptions.PlatformException(
                        error='400',
                        message='project_id must be strings')

                project = self.__get_by_id(project_id)
                # verify input project name is same as the given id
                if project_name is not None and project.name != project_name:
                    logger.warning(
                        "Mismatch found in projects.get: project_name is different then project.name:"
                        " {!r} != {!r}".format(
                            project_name,
                            project.name))
            elif project_name is not None:
                if not isinstance(project_name, str):
                    raise exceptions.PlatformException(
                        error='400',
                        message='project_name must be strings')

                projects = self.list()
                project = [project for project in projects if project.name == project_name]
                if not project:
                    # list is empty
                    raise exceptions.PlatformException(error='404',
                                                       message='Project not found. Name: {}'.format(project_name))
                    # project = None
                elif len(project) > 1:
                    # more than one matching project
                    raise exceptions.PlatformException(
                        error='404',
                        message='More than one project with same name. Please "get" by id')
                else:
                    project = project[0]
            else:
                raise exceptions.PlatformException(
                    error='404',
                    message='No input and no checked-out found')
        else:
            project = entities.Project.from_json(_json={'id': project_id,
                                                        'name': project_name},
                                                 client_api=self._client_api,
                                                 is_fetched=False)
        assert isinstance(project, entities.Project)
        if checkout:
            self.checkout(project=project)
        return project

    def delete(self,
               project_name: str = None,
               project_id: str = None,
               sure: bool = False,
               really: bool = False) -> bool:
        """
        Delete a project forever!
        :param project_name: optional - search by name
        :param project_id: optional - search by id
        :param sure: are you sure you want to delete?
        :param really: really really?

        :return: True
        """
        if sure and really:
            if project_id is None:
                project = self.get(project_name=project_name)
                project_id = project.id
            success, response = self._client_api.gen_request(req_type='delete',
                                                             path='/projects/{}'.format(project_id))
            if not success:
                raise exceptions.PlatformException(response)
            logger.info('Project id {} deleted successfully'.format(project_id))
            return True
        else:
            raise exceptions.PlatformException(
                error='403',
                message='Cant delete project from SDK. Please login to platform to delete')

    def update(self,
               project: entities.Project,
               system_metadata: bool = False) -> entities.Project:
        """
        Update a project
        :param project:
        :param system_metadata: True, if you want to change metadata system
        :return: Project object
        """
        url_path = '/projects/{}'.format(project.id)
        if system_metadata:
            url_path += '?system=true'
        success, response = self._client_api.gen_request(req_type='patch',
                                                         path=url_path,
                                                         json_req=project.to_json())
        if success:
            return project
        else:
            raise exceptions.PlatformException(response)

    def create(self,
               project_name: str,
               checkout: bool = False) -> entities.Project:
        """
        Create a new project
        :param project_name:
        :param checkout:
        :return: Project object
        """
        payload = {'name': project_name}
        success, response = self._client_api.gen_request(req_type='post',
                                                         path='/projects',
                                                         data=payload)
        if success:
            project = entities.Project.from_json(client_api=self._client_api,
                                                 _json=response.json())
        else:
            raise exceptions.PlatformException(response)
        assert isinstance(project, entities.Project)
        if checkout:
            self.checkout(project=project)
        return project
