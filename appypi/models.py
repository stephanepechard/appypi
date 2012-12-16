# -*- coding: utf-8 -*-
""" Files containing appypi model classes. """

# appypi
from appypi import settings

# sqlalchemy
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class AppypiDatabase(object):
    """ appypi database class. """

    def __init__(self):
        """ Init the database connection, kept all along the object's life. """
        db_path = 'sqlite:///' + settings.APPYPI_DB_PATH
        self.engine = create_engine(db_path, echo=settings.DEBUG)
        apps_table = Application.__table__
        metadata = Base.metadata
        metadata.create_all(self.engine)
        session_class = sessionmaker(bind=self.engine)
        self.session = session_class()

    def add_app(self, app):
        """ Add an app to the database. """
        self.session.add(app)
        self.session.commit()

    def remove_app(self, app):
        """ Remove an app from the database. """
        self.session.delete(app)
        self.session.commit()

    def app_is_installed(self, name):
        """ Check if an app is already in the database. """
        installed = None
        query = self.session.query(Application)
        results = query.filter(Application.name == name.lower()).all()
        if len(results) == 1:
            installed = results[0]
        return installed

    def installed_packages(self):
        """ Return the list apps present in the database. """
        return self.session.query(Application).all()

    def save(self):
        """ Save the model. """
        self.session.commit()


class Application(Base):
    """ Class representing an appypi application creation. """

    __tablename__ = 'Application'

    name = Column(String, primary_key=True)
    app_dir = Column(String)
    author = Column(String)
    description = Column(String)
    summary = Column(String)
    binfiles = Column(String)
    homepage = Column(String)
    installed_version = Column(String)
    real_name = Column(String)  # not lowered

    def __init__(self, package_name):
        self.name = package_name

    def __repr__(self):
        return "<Application('%s')>" % (self.name)

    def add_binfile(self, binfile):
        """ Add a binfile to the app. """
        if self.binfiles:
            self.binfiles = self.binfiles + ':' + binfile
        else:
            self.binfiles = binfile