from setuptools import setup, find_packages

setup(
    name="iotile_support_prod_pod1m_0",
    packages=find_packages(include=["iotile_support_prod_pod1m_0.*", "iotile_support_prod_pod1m_0"]),
    version="0.4.0rc2",
    install_requires=['iotile_support_con_nrf52832_3 ~= 3.1.9rc2', 'iotile_support_firm_accelerometer_2 ~= 2.3.5rc3', 'iotile_support_firm_env_1 ~= 1.1.1', u'sortedcontainers ~= 2.1'],
    entry_points={'iotile.app': ['tracker_app = iotile_support_prod_pod1m_0.tracker_app'], 'iotile.recipe_action': ['CalibratePOD1MStep = iotile_support_prod_pod1m_0.calibrate_pod1m_step:CalibratePOD1MStep', 'ResetPOD1MStep = iotile_support_prod_pod1m_0.reset_pod1m_step:ResetPOD1MStep']},
    author="Arch",
    author_email="info@arch-iot.com"
)