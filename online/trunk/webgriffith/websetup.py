"""Setup the WebGriffith application"""
import logging

from webgriffith.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup webgriffith here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Load the models
    from webgriffith.model import meta
    meta.metadata.bind = meta.engine

    # Create the tables if they aren't there already
    meta.metadata.create_all(checkfirst=True)
