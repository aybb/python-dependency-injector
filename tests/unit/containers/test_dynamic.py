"""Dependency injector dynamic container unit tests."""

import unittest2 as unittest

from dependency_injector import (
    containers,
    providers,
    errors,
)


class ContainerA(containers.DeclarativeContainer):
    p11 = providers.Provider()
    p12 = providers.Provider()


class DeclarativeContainerInstanceTests(unittest.TestCase):

    def test_providers_attribute(self):
        container_a1 = ContainerA()
        container_a2 = ContainerA()

        self.assertIsNot(container_a1.p11, container_a2.p11)
        self.assertIsNot(container_a1.p12, container_a2.p12)
        self.assertNotEqual(container_a1.providers, container_a2.providers)

    def test_set_get_del_providers(self):
        p13 = providers.Provider()

        container_a1 = ContainerA()
        container_a2 = ContainerA()

        container_a1.p13 = p13
        container_a2.p13 = p13

        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))
        self.assertEqual(ContainerA.cls_providers, dict(p11=ContainerA.p11,
                                                        p12=ContainerA.p12))

        self.assertEqual(container_a1.providers, dict(p11=container_a1.p11,
                                                      p12=container_a1.p12,
                                                      p13=p13))
        self.assertEqual(container_a2.providers, dict(p11=container_a2.p11,
                                                      p12=container_a2.p12,
                                                      p13=p13))

        del container_a1.p13
        self.assertEqual(container_a1.providers, dict(p11=container_a1.p11,
                                                      p12=container_a1.p12))

        del container_a2.p13
        self.assertEqual(container_a2.providers, dict(p11=container_a2.p11,
                                                      p12=container_a2.p12))

        del container_a1.p11
        del container_a1.p12
        self.assertEqual(container_a1.providers, dict())
        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))

        del container_a2.p11
        del container_a2.p12
        self.assertEqual(container_a2.providers, dict())
        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))

    def test_set_invalid_provider_type(self):
        container_a = ContainerA()
        container_a.provider_type = providers.Object

        with self.assertRaises(errors.Error):
            container_a.px = providers.Provider()

        self.assertIs(ContainerA.provider_type,
                      containers.DeclarativeContainer.provider_type)

    def test_override(self):
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        container = _Container()
        overriding_container1 = _OverridingContainer1()
        overriding_container2 = _OverridingContainer2()

        container.override(overriding_container1)
        container.override(overriding_container2)

        self.assertEqual(container.overridden,
                         (overriding_container1,
                          overriding_container2))
        self.assertEqual(container.p11.overridden,
                         (overriding_container1.p11,
                          overriding_container2.p11))

        self.assertEqual(_Container.overridden, tuple())
        self.assertEqual(_Container.p11.overridden, tuple())

    def test_override_with_itself(self):
        container = ContainerA()
        with self.assertRaises(errors.Error):
            container.override(container)

    def test_reset_last_overridding(self):
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        container = _Container()
        overriding_container1 = _OverridingContainer1()
        overriding_container2 = _OverridingContainer2()

        container.override(overriding_container1)
        container.override(overriding_container2)
        container.reset_last_overriding()

        self.assertEqual(container.overridden,
                         (overriding_container1,))
        self.assertEqual(container.p11.overridden,
                         (overriding_container1.p11,))

    def test_reset_last_overridding_when_not_overridden(self):
        container = ContainerA()

        with self.assertRaises(errors.Error):
            container.reset_last_overriding()

    def test_reset_override(self):
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        container = _Container()
        overriding_container1 = _OverridingContainer1()
        overriding_container2 = _OverridingContainer2()

        container.override(overriding_container1)
        container.override(overriding_container2)
        container.reset_override()

        self.assertEqual(container.overridden, tuple())
        self.assertEqual(container.p11.overridden, tuple())


if __name__ == '__main__':
    unittest.main()
